#!/usr/bin/python
import boto3
from infrastructure.interface import Infrastructure
import json

# ============================================================================ #
# Infrastructure via Amazon Web Services
# ============================================================================ #
class Platform(Infrastructure):
    # =-=-=--=---=-----=--------=-------------=
    # Functions
    # ----------------------------------------=
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.system_status_ok = self.ec2.get_waiter('system_status_ok')
        Infrastructure.__init__(self)
    
    def create_server(self):
        # create the instances
        num_instance = 2
        args = {
            'LaunchTemplate': {
                'LaunchTemplateName': 'stage_WebServer',
                'Version': '4'
            },
            'MaxCount': num_instance,
            'MinCount': num_instance
        }
        resp = self.ec2.run_instances(** args)
        list_instance = []
        for obj in resp['Instances']:
            list_instance.append(obj['InstanceId'])
        
        # wait for all instances to spin up
        self.system_status_ok.wait(InstanceIds=list_instance)
        
        # collect info to return
        resp = self.ec2.describe_instances(InstanceIds=list_instance)
        _return = {}
        
        _continue = True
        _continue = _continue and ('Reservations' in resp)
        _continue = _continue and (len(resp['Reservations']) != 0)
        _continue = _continue and ('Instances' in resp['Reservations'][0])
        
        if _continue == True:
            for obj in resp['Reservations'][0]['Instances']:
                _return[obj['InstanceId']] = obj['PublicDnsName']
            
        return _return
    
    def remove_server(self, KEY):
        """
            :param KEY - list or string, of instance(s) to be terminated
        """
        list_key = [KEY]
        if isinstance(KEY, list) == True:
            list_key = KEY
            
        resp = self.ec2.terminate_instances(InstanceIds=list_key)
        print json.dumps(resp, indent=4, sort_keys=True, default=str)