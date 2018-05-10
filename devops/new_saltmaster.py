#!/usr/bin/python
from infrastructure import platform_aws as provider
from util import ssh

cloud = provider.Platform()

HOST = "ec2-54-193-14-166.us-west-1.compute.amazonaws.com"
LIST_CMD = cloud.recipe_saltmaster
IDENTITY = "mserrano-stage.pem"

ssh.call(HOST, LIST_CMD, IDENTITY)

print 'hello world of bin'