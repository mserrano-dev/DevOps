#!/usr/bin/python
from infrastructure import platform_aws as provider
from infrastructure.polling import Polling
import json
import os
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
    stopwatch = timer.Stopwatch()

    cloud = provider.Platform()
    infrastructure = assign_roles(cloud.create_server(3))
    project_fs.upsert_file('infrastructure.json', json.dumps(infrastructure, indent=4))
    
    all_instance = infrastructure['webserver'] + infrastructure['saltmaster']
    list_host = array_column(all_instance, 'HOST')
    authenticate_all_host(list_host)
    
    install_saltstack(cloud, infrastructure)
    configure_saltstack(cloud, infrastructure)

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
    id_file = "mserrano-stage.pem"
    runner = multi_thread.Runner()
    for obj in infrastructure['saltmaster']:
        runner.add_task(name=obj['KEY'], target=ssh.call, args=(obj['HOST'], cloud.recipe_saltmaster, id_file,))
    for obj in infrastructure['webserver']:
        runner.add_task(name=obj['KEY'], target=ssh.call, args=(obj['HOST'], cloud.recipe_webserver, id_file,))
    runner.invoke_all_and_wait()

def configure_saltstack(cloud, infrastructure):
    pass
    
def authenticate_all_host(list_instance):
    authentication = Polling(2, 'Adding fingerprints to ~/ssh/known_hosts...', '...DONE')
    authentication.register_polling_fn(ssh.add_fingerprint)
    authentication.register_resp_parser_fn(confirm_success, {'list_instance': list_instance})
    authentication.register_resp_status_fn(report_progress, {'list_instance': list_instance})
    authentication.wait({'LIST_HOST':list_instance})
    
# =-=-=--=---=-----=--------=-------------=
# Helpers
# ----------------------------------------=
def confirm_success(resp, list_instance):
    _return = True
    if resp.count('\n') == (len(list_instance) * 3):
        out_file = open("%s/.ssh/known_hosts" % os.path.expanduser("~"), "a")
        out_file.write(resp)
    else:
        _return = False
        
    return _return

def report_progress(resp, list_instance):
    result = resp.count('\n') / 3
    if result == len(list_instance):
        _return = 'Success! %d/%d keys collected. Permanently adding to known_hosts..' % (result, len(list_instance))
    else:
        _return = 'Failed.. %d/%d. Trying again' % (result, len(list_instance))
    return _return

main() # start script