#!/usr/bin/python
import sys
from util import output
from util import remote_host
from util import timer
from util.array_phpfill import *

# ============================================================================ #
# Deploy selected app to all webservers
# ============================================================================ #
def main():
    stopwatch = timer.Stopwatch()
    
    git_repo = sys.argv[1]
    deploy_app(git_repo)
    
    stopwatch.output_report()

# =-=-=--=---=-----=--------=-------------=
# Helpers
# ----------------------------------------=
def deploy_app(git_repo):
    list_cmd = [
        "sudo", "salt", "-G", "roles:webserver*",
        "state.apply", "webserver.update_app",
        "pillar={\"git_repo\": \"%s\"}" % git_repo
    ]
    remote_host.local(list_cmd)

main() # start script
