#!/usr/bin/python
import os
import subprocess
from util import project_fs
from util.polling import Polling

# ============================================================================ #
# Remote Host related helpers
#   NOTE: assumes identity file in directory ~/.ssh
# ============================================================================ #
def ssh(HOST, IDENTITY, LIST_CMD):
    """
    Execute commands on remote host
    """
    args = [
        "ssh", "-T",
        "-i", "%s/.ssh/%s" % (os.path.expanduser("~"), IDENTITY), 
        "ubuntu@%s" % HOST, ' && '.join(LIST_CMD)
    ]
    return subprocess.Popen(args).wait()

def rsync(HOST, IDENTITY, SOURCE, DESTINATION):
    """
    Syncs a remote file to local destination
    """
    args = [
        "rsync",
        "-e", 'ssh -i %s/.ssh/%s' % (os.path.expanduser("~"), IDENTITY),
        "ubuntu@%s:%s" % (HOST, SOURCE),
        '%s/%s' % (project_fs.get_root(), DESTINATION),
    ]
    return subprocess.Popen(args).wait()

def local(LIST_CMD):
    """
    Execute commands on local host
    
    """
    return subprocess.Popen(LIST_CMD).wait()

def add_knownhosts( ** kwargs):
    """
    Adds all listed host to known_hosts file via polling
        :kwarg title_msg - <String>
        :kwarg list_host - [<String>]
        :kwarg done_msg - <String>
    """
    def auth_confirm_success(resp, list_host):
        ''' Write to known hosts '''
        _return = True
        if resp.count('\n') == (len(list_host) * 3):
            out_file = open("%s/.ssh/known_hosts" % os.path.expanduser("~"), "a")
            out_file.write(resp)
        else:
            _return = False
        return _return
    
    def auth_report_progress(resp, list_host):
        ''' Report how many keys available '''
        result = resp.count('\n') / 3
        if result == len(list_host):
            _return = 'Success! %d/%d keys collected. Permanently adding to known_hosts..' % (result, len(list_host))
        else:
            _return = 'Failed.. %d/%d keys collected. Trying again' % (result, len(list_host))
        return _return
    
    def poll_authentication(LIST_HOST):
        ''' Attempt to retrieve all fingerprints from LIST_HOST '''
        args = [
            "ssh-keyscan", "-H", "-4",
        ] + LIST_HOST

        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        process.wait()
        return process.stdout.read()
    
    status_auth = Polling(polling_interval=2,
                          polling_function=poll_authentication,
                          start_msg=kwargs['title_msg'], 
                          end_msg=kwargs['done_msg'])
    status_auth.register_resp_parser_fn(auth_confirm_success, {'list_host':kwargs['list_host']})
    status_auth.register_resp_status_fn(auth_report_progress, {'list_host':kwargs['list_host']})
    status_auth.wait({'LIST_HOST':kwargs['list_host']})
