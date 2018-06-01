#!/usr/bin/python
import argparse
from infrastructure import settings as helper
import sys
from util import output
from util import remote_host
from util import timer
from util.array_phpfill import *

# ============================================================================ #
# Verify identity, then invoke requested script
# ============================================================================ #
def main():
    """
    pipenv run python devops/remote_dispatcher.py   ROLE   SCRIPT   ARGS  
        :param -r ROLE - name of bin subdir holding the script
        :param -s SCRIPT - name of script to invoke
        :param -a ARGS - any args to invoke with script, as a string
    """
    stopwatch = timer.Stopwatch()
    
    parsed = use_argparse()
    settings = helper.get_mserrano_config()
    
    list_cmd = [
        "/media/DevOps/bin/%s/%s %s" % (parsed.role, parsed.script, parsed.args),
    ]
    remote_host.ssh("mserrano.net", settings["OpsIdentity"], list_cmd)
    
    stopwatch.output_report()

# =-=-=--=---=-----=--------=-------------=
# Helpers
# ----------------------------------------=
def use_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--role',
                        action="store", dest="role",
                        help="bin subdir/minion role")
    parser.add_argument('-s', '--script',
                        action="store", dest="script",
                        help="script to be executed")
    parser.add_argument('-a', '--args',
                        action="store", dest="args",
                        help="script arguments as a string")
    return parser.parse_args()

main() # start script
