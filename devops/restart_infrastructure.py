#!/usr/bin/python
from infrastructure import platform_aws as provider
import json
import os
import re
import sys
from termcolor import colored
from util import date
from util import multi_thread
from util import project_fs
from util import remote_host
from util import timer
from util.array_phpfill import *
from util.polling import Polling

# ============================================================================ #
# Setup new saltmaster and webserver ec2 instances. 
# Garbage collect remaining servers if all tests passing.
# ============================================================================ #
def main():
    settings = {
        # infrastructure settings
        'Count': 3,
        # aws specific settings
        'Template': 'ubuntu_18.04',
        'Version': '1',
    }
    stopwatch = timer.Stopwatch()
    
    cloud = provider.Platform(settings)
    infrastructure = assign_roles(cloud.create_server(settings['Count']))
    project_fs.upsert_file('infrastructure.json', json.dumps(infrastructure, indent=4))
    cloud.list_saltmaster = array_column(infrastructure['saltmaster'], 'IP')
    cloud.id_file = "mserrano-stage.pem"
    
    all_instance = infrastructure['webserver'] + infrastructure['saltmaster']
    list_host = array_column(all_instance, 'IP')
    authenticate_all_host(list_host)
    
    install_saltstack(cloud, infrastructure)
    configure_minion(cloud, infrastructure)
    configure_master(cloud, infrastructure)
    install_docker(cloud, infrastructure)
    run_webservers(cloud, infrastructure)
    
    stopwatch.output_report()

# =-=-=--=---=-----=--------=-------------=
# Functions
# ----------------------------------------=
def assign_roles(list_instance):
    _return = {
        'interface': provider.__name__,
        'date_created': date.today(),
        'saltmaster':[list_instance.pop()],
        'webserver': list_instance,
    }
    return _return

def authenticate_all_host(list_host):
    authentication = Polling(2, 'Adding fingerprints to ~/ssh/known_hosts...', '...DONE (All Remote Host Authenticated)')
    authentication.register_polling_fn(remote_host.add_fingerprint)
    authentication.register_resp_parser_fn(auth_confirm_success, {'list_host': list_host})
    authentication.register_resp_status_fn(auth_report_progress, {'list_host': list_host})
    authentication.wait({'LIST_HOST':list_host})

def install_saltstack(cloud, infrastructure):
    runner = multi_thread.Runner()
    runner.add_recipe_on_each(cloud, infrastructure['saltmaster'], 'saltstack_master')
    runner.add_recipe_on_each(cloud, infrastructure['webserver'], 'saltstack_minion')
    runner.invoke_all_and_wait()
    output_done_msg('Saltstack Installed')

def configure_webserver_minion(cloud, infrastructure):
    run_on_each(cloud, infrastructure['webserver'], 'configure_minion', 'Minions Configured')

def configure_master_as_minion(cloud, infrastructure):
    run_on_each(cloud, infrastructure['saltmaster'], 'configure_master_as_minion', 'Master Configured as Minion')

def configure_minion(cloud, infrastructure):
    configure_webserver_minion(cloud, infrastructure)
    configure_master_as_minion(cloud, infrastructure)

def configure_master(cloud, infrastructure):
    run_on_each(cloud, infrastructure['saltmaster'], 'configure_master', 'Applying Highstate to each Minion')

def install_docker(cloud, infrastructure):
    status_docker = Polling(10, 'Setting up Docker...', '...DONE (All Docker daemon now running)')
    status_docker.register_polling_fn(remote_host.rsync)
    status_docker.register_resp_parser_fn(docker_confirm_success, {'cloud': cloud})
    status_docker.register_resp_status_fn(docker_report_progress, {'cloud': cloud})
    args = {
        'HOST': cloud.list_saltmaster[0],
        'IDENTITY': cloud.id_file,
        'SOURCE': cloud.log_location_on_remote,
        'DESTINATION': cloud.log_location_on_local,
    }
    status_docker.wait(args)

def run_webservers(cloud, infrastructure):
    status_web = Polling(5, 'Creating docker images...', '...DONE (All Apache2 server now running and ready to serve traffic)')
    status_web.register_polling_fn(remote_host.rsync)
    status_web.register_resp_parser_fn(web_confirm_success, {'cloud': cloud})
    status_web.register_resp_status_fn(web_report_progress, {'cloud': cloud})
    args = {
        'HOST': cloud.list_saltmaster[0],
        'IDENTITY': cloud.id_file,
        'SOURCE': cloud.log_location_on_remote,
        'DESTINATION': cloud.log_location_on_local,
    }
    status_web.wait(args)

# =-=-=--=---=-----=--------=-------------=
# Helpers
# ----------------------------------------=
def run_on_each(cloud, list_instance, recipe, msg):
    runner = multi_thread.Runner()
    runner.add_recipe_on_each(cloud, list_instance, recipe)
    runner.invoke_all_and_wait()
    output_done_msg(msg)

def output_done_msg(msg):
    print colored('  >', 'cyan', attrs=['blink']) + colored(' ...DONE', 'cyan') + ' (%s)' % msg, '\r',
    sys.stdout.flush()
    timer.sleep(1)
    print colored('  > ...DONE (%s)' % msg, 'cyan')

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

def count_occurances(file, search_key):
    haystack = project_fs.read_file_safe(file, '')
    needle = '(%s)' % search_key
    result = re.findall(needle, haystack)
    
    return len(result)

def presence_in_file(file, search_key, expected_count):
    num_found = count_occurances(file, search_key)
    
    return (num_found == expected_count)

def docker_confirm_success(resp, cloud):
    args = {
        'file': cloud.log_location_on_local,
        'search_key': 'minion setup',
        'expected_count': cloud.count_webserver
    }
    return presence_in_file(** args)

def docker_report_progress(resp, cloud):
    args = {
        'file': cloud.log_location_on_local,
        'search_key': 'minion setup',
    }
    msg = 'are now ready'
    return '%s/%s %s' % (count_occurances(** args), cloud.count_webserver, msg)

def web_confirm_success(resp, cloud):
    args = {
        'file': cloud.log_location_on_local,
        'search_key': 'minion running',
        'expected_count': cloud.count_webserver
    }
    return presence_in_file(** args)

def web_report_progress(resp, cloud):
    args = {
        'file': cloud.log_location_on_local,
        'search_key': 'minion running',
    }
    msg = 'are running containers successfully'
    return '%s/%s %s' % (count_occurances(** args), cloud.count_webserver, msg)

main() # start script
