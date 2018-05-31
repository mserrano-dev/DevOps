#!/usr/bin/python
import boto3
import json
from util import project_fs
from util import timer
from util.array_phpfill import *

# ============================================================================ #
# Amazon Simple Storage Service (S3) Bucket
# ============================================================================ #
class S3Bucket():
    __devops_bucket = 'mserrano-devops-bucket'
    
    # =-=-=--=---=-----=--------=-------------=
    # Functions
    # ----------------------------------------=
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.__upsert_devops_bucket()
    
    def upsert_file(self, filename):
        """
        Add object or update if it already exists
            :param filepath - path of file to put into bucket
        """
        bucket = self.__devops_bucket
        filepath = '%s/%s' % (project_fs.get_root(), filename)
        response = self.s3.upload_file(filepath, bucket, filename)
    
    def get_file(self, bucket_name, filename):
        """
        Retrieve stored file contents
            :param filename - file to be retrieved
        """
        args = {
            'Bucket': bucket_name,
            'Key': filename
        }
        response = self.s3.get_object( ** args)
        return response['Body'].read()        
    
    def get_devops_file(self, filename):
        """
        Retrieve stored json file as python object
            :param filename - file to be retrieved
        """
        file_content = self.get_file(self.__devops_bucket, filename)
        return json.loads(file_content)
    
    # =-=-=--=---=-----=--------=-------------=
    # Helpers
    # ----------------------------------------=
    def __upsert_devops_bucket(self):
        """
        Creates bucket if it does not already exist
        """
        response = self.s3.list_buckets()
        list_owned_buckets = array_column(response['Buckets'], 'Name')
        bucket_does_not_exist = (self.__devops_bucket not in list_owned_buckets)
        if bucket_does_not_exist:
            endpoint = self.infrastructure['loadbalancer'][0]['REGION']
            args = {
                'Bucket': self.__devops_bucket,
                'CreateBucketConfiguration': {
                    'LocationConstraint': self.__strip_specific_endpoint(endpoint),
                },
            }
            response = self.s3.create_bucket( ** args)
    
    def __strip_specific_endpoint(self, specific_region_endpoint):
        components = specific_region_endpoint.split('-')
        components[-1] = filter(lambda x: x.isdigit(), components[-1])
        return '-'.join(components)
