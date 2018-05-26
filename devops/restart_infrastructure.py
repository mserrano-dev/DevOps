#!/usr/bin/python
from infrastructure import dns_server
from infrastructure import platform_aws as provider
import json
import os
import re
import sys
from termcolor import colored
from util import date
from util import multi_thread
from util import output
from util import project_fs
from util import remote_host
from util import timer
from util.array_phpfill import *
from util.polling import Polling

# ============================================================================ #
# Setup new saltmaster/loadbalancer and webserver ec2 instances.
# Garbage collect remaining servers if all tests passing.
# ============================================================================ #
def main():
    stopwatch = timer.Stopwatch()
    
    settings = project_fs.read_json('.aws/mserrano.config', rel_to_user_home=True)
    cloud = provider.Platform(settings)
    infrastructure = assign_roles(cloud.create_server(settings['ServerCount']))
    project_fs.upsert_file('infrastructure.json', json.dumps(infrastructure, indent=4))
    cloud.id_file = settings['Identity']
    cloud.ip_haproxy = array_column(infrastructure['loadbalancer'], 'IP')[0]
    cloud.list_saltmaster = array_column(infrastructure['saltmaster'], 'IP')
    cloud.list_webserver = array_column(infrastructure['webserver'], 'IP')
    
    all_instance = infrastructure['webserver'] + infrastructure['saltmaster']
    list_host = array_column(all_instance, 'IP')
    authenticate_all_host(list_host)
    
    install_saltstack(cloud, infrastructure)
    configure_minion(cloud, infrastructure)
    configure_master(cloud, infrastructure)
    configure_haproxy(cloud, infrastructure)
    install_docker(cloud, infrastructure)
    run_webservers(cloud, infrastructure)
    point_to_loadbalancer(cloud, infrastructure)
    do_garbage_collect(cloud, infrastructure)
    
    stopwatch.output_report()

# =-=-=--=---=-----=--------=-------------=
# Functions
# ----------------------------------------=
def assign_roles(list_instance, count_master=0):
    count = min(count_master, 1)
    
    list_web = list_instance[count + 1:]
    list_master = list_instance[:count + 1]
    haproxy = list_master[0]
    
    _return = {
        'interface': provider.__name__,
        'date_created': date.today(),
        'loadbalancer':[haproxy],
        'saltmaster':list_master,
        'webserver': list_web,
    }
    return _return

def authenticate_all_host(list_host):
    poll_authentication(title_msg='Adding fingerprints to ~/ssh/known_hosts...', 
                        list_host=list_host,
                        done_msg='All Remote Host Authenticated')

def install_saltstack(cloud, infrastructure):
    runner = multi_thread.Runner()
    runner.add_recipe_on_each(cloud, infrastructure['saltmaster'], 'saltstack_master')
    runner.add_recipe_on_each(cloud, infrastructure['webserver'], 'saltstack_minion')
    runner.invoke_all_and_wait()
    output.end_banner('Saltstack Installed')

def configure_webserver_minion(cloud, infrastructure):
    run_on_each(cloud, infrastructure['webserver'],
                recipe='configure_minion',
                status_msg='Minions Configured')

def configure_master_as_minion(cloud, infrastructure):
    run_on_each(cloud, infrastructure['saltmaster'],
                recipe='configure_master_as_minion',
                status_msg='Master Configured as Minion')

def configure_minion(cloud, infrastructure):
    configure_webserver_minion(cloud, infrastructure)
    configure_master_as_minion(cloud, infrastructure)

def configure_master(cloud, infrastructure):
    run_on_each(cloud, infrastructure['saltmaster'],
                recipe='configure_master',
                status_msg='Accepted all Minion public keys and Applied a Highstate')

def configure_haproxy(cloud, infrastructure):
    poll_highstate_status(cloud, infrastructure,
                          polling_interval=20,
                          search_key='haproxy running',
                          expected=len(infrastructure['loadbalancer']),
                          title_msg='Setting up more processing capacity...',
                          status_msg='HAProxy daemon running',
                          done_msg='Load Balancer ready to provide high availability')

def install_docker(cloud, infrastructure):
    poll_highstate_status(cloud, infrastructure,
                          polling_interval=4,
                          search_key='minion setup',
                          expected=len(infrastructure['webserver']),
                          title_msg='Setting up Docker...',
                          status_msg='Docker daemon running',
                          done_msg='All Docker daemon ready to accept Docker CLI commands')

def run_webservers(cloud, infrastructure):
    poll_highstate_status(cloud, infrastructure,
                          polling_interval=6,
                          search_key='minion running',
                          expected=len(infrastructure['webserver']),
                          title_msg='Docker CLI is creating image to run...',
                          status_msg='are running containers successfully',
                          done_msg='All Apache2 server now running and ready to serve traffic')

def point_to_loadbalancer(cloud, infrastructure):
    route53 = dns_server.Route53(cloud.settings)
    route53.modify_record_set('*.mserrano.net', cloud.ip_haproxy)

def do_garbage_collect(cloud, infrastructure):
    list_active_server = cloud.list_server()
    list_infrastructure = array_unique(array_column(infrastructure['loadbalancer'], 'KEY')
                                       + array_column(infrastructure['saltmaster'], 'KEY')
                                       + array_column(infrastructure['webserver'], 'KEY'))
    list_garbage = array_diff(list_active_server, list_infrastructure)
    msg = 'Garbage Collected Successfully'
    if list_garbage != []:
        print '  Will terminate %s instances' % len(list_garbage)
        result = cloud.remove_server(list_garbage)
        if result == False:
            msg = "| \033[91m!! Garbage Collection Failed !!\033[0m\033[36m |"
    else:
        print '  Nothing to do here'
    output.end_banner(msg)

# =-=-=--=---=-----=--------=-------------=
# Helpers
# ----------------------------------------=
def run_on_each(cloud, list_instance, ** kwargs):
    runner = multi_thread.Runner()
    runner.add_recipe_on_each(cloud, list_instance, kwargs['recipe'])
    runner.invoke_all_and_wait()
    output.end_banner(kwargs['status_msg'])

def poll_authentication( ** kwargs):
    def auth_confirm_success(resp, list_host):
        _return = True
        if resp.count('\n') == (len(list_host) * 3):
            out_file = open("%s/.ssh/known_hosts" % os.path.expanduser("~"), "a")
            out_file.write(resp)
        else:
            _return = False
        return _return
    
    def auth_report_progress(resp, list_host):
        result = resp.count('\n') / 3
        if result == len(list_host):
            _return = 'Success! %d/%d keys collected. Permanently adding to known_hosts..' % (result, len(list_host))
        else:
            _return = 'Failed.. %d/%d keys collected. Trying again' % (result, len(list_host))
        return _return
    
    status_auth = Polling(polling_interval=2,
                          polling_function=remote_host.add_fingerprint,
                          start_msg=kwargs['title_msg'], 
                          end_msg=kwargs['done_msg'])
    status_auth.register_resp_parser_fn(auth_confirm_success, {'list_host':kwargs['list_host']})
    status_auth.register_resp_status_fn(auth_report_progress, {'list_host':kwargs['list_host']})
    status_auth.wait({'LIST_HOST':kwargs['list_host']})

def poll_highstate_status(cloud, infrastructure, ** kwargs):
    def __count_occurances(file, search_key):
        haystack = project_fs.read_file_safe(file, '')
        needle = '(%s)' % search_key
        matches = re.findall(needle, haystack)
        return len(matches)
    
    def highstate_confirm_success(resp, cloud, search_key):
        num_found = __count_occurances(cloud.log_location_on_local, search_key)
        return (num_found == kwargs['expected'])
    
    def highstate_report_progress(resp, cloud, search_key):
        num_found = __count_occurances(cloud.log_location_on_local, search_key)
        return '%s/%s %s' % (num_found, kwargs['expected'], kwargs['status_msg'])
    
    status_highstate = Polling(polling_interval=kwargs['polling_interval'],
                               polling_function=remote_host.rsync,
                               start_msg=kwargs['title_msg'],
                               end_msg=kwargs['done_msg'])
    status_highstate.register_resp_parser_fn(highstate_confirm_success, {'cloud': cloud, 'search_key': kwargs['search_key']})
    status_highstate.register_resp_status_fn(highstate_report_progress, {'cloud': cloud, 'search_key': kwargs['search_key']})
    args = {
        'HOST': cloud.list_saltmaster[0],
        'IDENTITY': cloud.id_file,
        'SOURCE': cloud.log_location_on_remote,
        'DESTINATION': cloud.log_location_on_local,
    }
    status_highstate.wait(args)

main() # start script
