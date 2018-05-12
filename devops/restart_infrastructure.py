#!/usr/bin/python
from infrastructure import platform_aws as provider
from infrastructure.polling import Polling
import os
from util import multi_thread
from util import ssh
from util import timer

# ============================================================================ #
# Setup new saltmaster and webserver ec2 instances. 
# Garbage collect remaining servers if all tests passing.
# ============================================================================ #
def main():
    stopwatch = timer.Stopwatch()

    cloud = provider.Platform()
    list_instance = cloud.create_server(3)

    authenticate_all_host(list_instance.values())
    install_saltstack(list_instance, cloud.recipe_saltmaster)

    stopwatch.output_report()
    
# =-=-=--=---=-----=--------=-------------=
# Functions
# ----------------------------------------=
def install_saltstack(list_instance, recipe):
    id_file = "mserrano-stage.pem"
    runner = multi_thread.Runner()
    for instance_id, host in list_instance.items():
        runner.add_task(name=instance_id, target=ssh.call, args=(host, recipe, id_file, ))
    runner.invoke_all_and_wait()
    
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