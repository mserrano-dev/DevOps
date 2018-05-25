#!/usr/bin/python
import boto3
from util.polling import Polling

# ============================================================================ #
# Scalable and Highly Available DNS Server via Route53
# ============================================================================ #
class Route53():
    # =-=-=--=---=-----=--------=-------------=
    # Functions
    # ----------------------------------------=
    def __init__(self, settings):
        self.settings = settings
        self.route53 = boto3.client('route53')
    
    def modify_record_set(self, RECORD, IP_ADDR):
        """
        Update dns record to have ip_addr as value
            :param RECORD - dns record to modify
            :param IP_ADDR - ip address to set value to
        """
        args = {
            'HostedZoneId': self.settings['HostedZoneId'],
            'ChangeBatch': {
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': RECORD,
                            'Type': 'A',
                            'ResourceRecords': [
                                {'Value': IP_ADDR},
                            ],
                            'TTL': 60,
                        },
                    },
                ]
            },
        }
        response = self.route53.change_resource_record_sets( ** args)
        self.__wait_until_insync(response['ChangeInfo']['Id'], IP_ADDR)
    
    # =-=-=--=---=-----=--------=-------------=
    # Helpers
    # ----------------------------------------=
    def __wait_until_insync(self, job_id, ip_addr):
        """
        Stop execution until Route53 propagates all changes
        """
        status_job = Polling(10, 'propagating changes to all Amazon Route53 authoritative DNS servers...', '...DONE (mserrano.net now pointing to %s' % ip_addr)
        status_job.register_polling_fn(self.route53.get_change)
        status_job.register_resp_parser_fn(self.__resp_parser, {})
        status_job.register_resp_status_fn(self.__resp_status, {})
        args = {
            'Id': job_id,
        }
        status_job.wait(args)
    
    def __resp_parser(self, resp):
        status = resp['ChangeInfo']['Status']
        return (status == 'INSYNC')
    
    def __resp_status(self, resp):
        status = resp['ChangeInfo']['Status']
        msg = {
            'PENDING': 'status pending, please wait...',
            'INSYNC': 'all DNS servers are in-sync',
        }
        return msg[status]
