#!/usr/bin/python
from infrastructure import platform_aws as provider
from util import ssh

cloud = provider.Platform()
list_instance = cloud.create_server()
print list_instance

install_saltmaster = cloud.recipe_saltmaster
id_file = "mserrano-stage.pem"
for instance_id, host in list_instance.items():
    ssh.call(host, install_saltmaster, id_file)

print 'hello world of bin'