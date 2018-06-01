#!/usr/bin/python
import sys
from util import remote_host
from util import timer

# ============================================================================ #
# Remove old RSA host key and add new one
# ============================================================================ #
def main():
    stopwatch = timer.Stopwatch()
    
    known_host = "mserrano.net"
    update_fingerprint(known_host)
    
    stopwatch.output_report()

# =-=-=--=---=-----=--------=-------------=
# Functions
# ----------------------------------------=
def update_fingerprint(HOST):
    remove_key(HOST)
    add_key(HOST)

def remove_key(HOST):
    list_cmd = [
        "ssh-keygen", "-R", HOST
    ]
    remote_host.local(list_cmd)

def add_key(HOST):
    remote_host.add_knownhosts(title_msg='Updating fingerprint of mserrano.net...', 
                               list_host=[HOST],
                               done_msg='New RSA Key added to ~/ssh/known_hosts')

main() # start script
