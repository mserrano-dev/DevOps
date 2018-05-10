#!/usr/bin/python
import boto3
from infrastructure.interface import Infrastructure
import json

# ============================================================================ #
# Infrastructure via Amazon Web Services
# ============================================================================ #
class Platform(Infrastructure):
    
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        Infrastructure.__init__(self)
    
    def create_server(self):
        return
    
    def remove_server(self, KEY):
        list_key = [KEY]
        if isinstance(KEY, 'list') == True:
            list_key = KEY
            
        resp = self.ec2.terminate_instances(InstanceIds=list_key)
        print json.dumps(resp, indent=4, sort_keys=True, default=str)

        