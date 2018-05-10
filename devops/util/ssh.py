#!/usr/bin/python
import os
import subprocess

def call(HOST, LIST_CMD, IDENTITY):
    # Execute commands on remote host
    #   NOTE: assumes identity file in directory ~/.ssh
    args = [
        "ssh", "-t", 
        "-i", "%s/.ssh/%s" % (os.path.expanduser("~"), IDENTITY), 
        "ubuntu@%s" % HOST, ' && '.join(LIST_CMD)
    ]
    subprocess.Popen(args).wait()