#!/usr/bin/python

import awscli as aws
import os
import subprocess

HOST = "ec2-54-193-14-166.us-west-1.compute.amazonaws.com"
LIST_CMD = [
    'sudo apt update -y',
    'sudo apt upgrade -y',
    'sudo apt install cowsay -y',
    'cowsay "William is the Coolest!!"',
]

# Execute commands on remote host
args = [
    "ssh", "-t", 
    "-i", "%s/.ssh/mserrano-stage.pem" % os.path.expanduser("~"), 
    "ubuntu@%s" % HOST, ' && '.join(LIST_CMD)
]
subprocess.Popen(args).wait()