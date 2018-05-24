#!/usr/bin/python
import os
import subprocess

# ============================================================================ #
# Remote Host related helpers
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
      NOTE: assumes identity file in directory ~/.ssh
    """
    args = [
        "ssh", "-T",
        "-i", "%s/.ssh/%s" % (os.path.expanduser("~"), IDENTITY), 
        "ubuntu@%s" % HOST, ' && '.join(LIST_CMD)
    ]
    return subprocess.Popen(args).wait()
