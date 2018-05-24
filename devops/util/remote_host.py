#!/usr/bin/python
import os
import subprocess
from util import project_fs

# ============================================================================ #
# Remote Host related helpers
#   NOTE: assumes identity file in directory ~/.ssh
# ============================================================================ #
def add_fingerprint(LIST_HOST):
    """
    Adds all listed host to known_hosts file
        :param LIST_HOST - [<String>]
    """
    args = [
        "ssh-keyscan", "-H", "-4",
    ] + LIST_HOST
    
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    process.wait()
    return process.stdout.read()

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
