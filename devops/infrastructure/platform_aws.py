#!/usr/bin/python
import boto3
from infrastructure.interface import Infrastructure
from infrastructure.polling import Polling
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
    
    def create_server(self, COUNT):
        # create the instances
        args = {
            'LaunchTemplate': {
                'LaunchTemplateName': 'stage_WebServer',
                'Version': '4'
            },
            'MaxCount': COUNT,
            'MinCount': COUNT
        }
        resp = self.ec2.run_instances( ** args)
        list_instance = []
        for obj in resp['Instances']:
            list_instance.append(obj['InstanceId'])
        
        # wait for all instances to spin up
        custom_waiter = Polling(5, 'Spinning up new servers...', '...DONE')
        custom_waiter.register_polling_fn(self.ec2.describe_instance_status)
        custom_waiter.register_resp_parser_fn(self.__resp_parser, {})
        custom_waiter.register_resp_status_fn(self.__resp_status, {})
        custom_waiter.wait({'InstanceIds': list_instance})
        
        # collect info to return
        resp = self.ec2.describe_instances(InstanceIds=list_instance)
        _return = []
        
        _continue = True
        _continue = _continue and ('Reservations' in resp)
        _continue = _continue and (len(resp['Reservations']) != 0)
        _continue = _continue and ('Instances' in resp['Reservations'][0])
        
        if _continue == True:
            for instance in resp['Reservations'][0]['Instances']:
                obj = {
                    'KEY': instance['InstanceId'], 
                    'HOST': instance['PublicDnsName'],
                }
                _return.append(obj)
            
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

    # =-=-=--=---=-----=--------=-------------=
    # Helpers
    # ----------------------------------------=
    def __resp_parser(self, resp):
        result = {}
        for obj in resp['InstanceStatuses']:
            status = obj['InstanceState']['Name']
            if status in result:
                result[status] += 1
            else:
                result[status] = 1
            
        _return = False
        if (len(result)) == 1 and ('running' in result):
            if (result['running'] == len(resp['InstanceStatuses'])):
                _return = True
                
        return _return
    
    def __resp_status(self, resp):
        result = {}
        for obj in resp['InstanceStatuses']:
            status = obj['InstanceState']['Name']
            if status in result:
                result[status] += 1
            else:
                result[status] = 1
        
        _return = ''
        if len(result) != 0:
            _return = '%s servers %s' % (result.values()[0], result.keys()[0])
            
        return _return