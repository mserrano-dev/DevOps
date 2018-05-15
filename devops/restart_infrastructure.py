#!/usr/bin/python
from infrastructure import platform_aws as provider
from infrastructure.polling import Polling
import json
import os
from termcolor import colored
from util import date
from util import multi_thread
from util import project_fs
from util import ssh
from util import timer
from util.array_phpfill import *

# ============================================================================ #
# Setup new saltmaster and webserver ec2 instances. 
# Garbage collect remaining servers if all tests passing.
# ============================================================================ #
def main():
    settings = {
        # infrastructure settings
        'Count': 3,
        # aws specific settings
        'Template': 'stage_WebServer',
        'Version': '4',
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
    configure_minions(cloud, infrastructure)
    install_webservers(cloud, infrastructure)

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

def install_saltstack(cloud, infrastructure):
    runner = multi_thread.Runner()
    for obj in infrastructure['saltmaster']:
        target_args = (obj['IP'], cloud.recipe('saltstack_master'), cloud.id_file, )
        runner.add_task(name=obj['KEY'], target=ssh.call, args=target_args)
    for obj in infrastructure['webserver']:
        target_args = (obj['IP'], cloud.recipe('saltstack_minion'), cloud.id_file, )
        runner.add_task(name=obj['KEY'], target=ssh.call, args=target_args)
    runner.invoke_all_and_wait()
    print colored('  ...DONE', 'cyan') + ' (Saltstack Installed)'
    
def configure_minions(cloud, infrastructure):
    runner = multi_thread.Runner()
    for obj in infrastructure['webserver']:
        target_args = (obj['IP'], cloud.recipe('configure_minion'), cloud.id_file, )
        runner.add_task(name=obj['KEY'], target=ssh.call, args=target_args)
    runner.invoke_all_and_wait()
    print colored('  ...DONE', 'cyan') + ' (Minions Configured)'
    
def install_webservers(cloud, infrastructure):
    runner = multi_thread.Runner()
    for obj in infrastructure['saltmaster']:
        target_args = (obj['IP'], cloud.recipe('setup_webserver'), cloud.id_file, )
        runner.add_task(name=obj['KEY'], target=ssh.call, args=target_args)
    runner.invoke_all_and_wait()
    print colored('  ...DONE', 'cyan') + ' (Webservers Setup)'
    
def authenticate_all_host(list_host):
    authentication = Polling(2, 'Adding fingerprints to ~/ssh/known_hosts...', '...DONE')
    authentication.register_polling_fn(ssh.add_fingerprint)
    authentication.register_resp_parser_fn(confirm_success, {'list_host': list_host})
    authentication.register_resp_status_fn(report_progress, {'list_host': list_host})
    authentication.wait({'LIST_HOST':list_host})
    
# =-=-=--=---=-----=--------=-------------=
# Helpers
# ----------------------------------------=
def confirm_success(resp, list_host):
    _return = True
    if resp.count('\n') == (len(list_host) * 3):
        out_file = open("%s/.ssh/known_hosts" % os.path.expanduser("~"), "a")
        out_file.write(resp)
    else:
        _return = False
    return _return

def report_progress(resp, list_host):
    result = resp.count('\n') / 3
    if result == len(list_host):
        _return = 'Success! %d/%d keys collected. Permanently adding to known_hosts..' % (result, len(list_host))
    else:
        _return = 'Failed.. %d/%d. Trying again' % (result, len(list_host))
    return _return

main() # start script