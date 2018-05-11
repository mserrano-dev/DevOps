#!/usr/bin/python
import os
import subprocess

# ============================================================================ #
# SSH related helpers
# ============================================================================ #
def add_fingerprint(LIST_HOST):
    """
    Adds all listed host to known_hosts file
        :param LIST_HOST - [<String>]
    """
    args = [
        "ssh-keyscan", "-H",
    ] + LIST_HOST
    
    out_file = open("%s/.ssh/known_hosts" % os.path.expanduser("~"), "a")
    subprocess.Popen(args, stdout=out_file).wait()
    
def call(HOST, LIST_CMD, IDENTITY):
    """
    Execute commands on remote host
      NOTE: assumes identity file in directory ~/.ssh
    """
    args = [
        "ssh", "-t", 
        "-i", "%s/.ssh/%s" % (os.path.expanduser("~"), IDENTITY), 
        "ubuntu@%s" % HOST, ' && '.join(LIST_CMD)
    ]
    subprocess.Popen(args).wait()