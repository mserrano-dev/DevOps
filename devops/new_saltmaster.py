#!/usr/bin/python
from infrastructure import platform_aws as provider
from time import time
from util import multi_thread
from util import ssh

ts = time()

cloud = provider.Platform()
list_instance = cloud.create_server()
print list_instance

install_saltmaster = cloud.recipe_saltmaster
id_file = "mserrano-stage.pem"
ssh.add_fingerprint(list_instance.values())

runner = multi_thread.Runner()
for instance_id, host in list_instance.items():
    runner.add_task(name=instance_id, target=ssh.call, args=(host, install_saltmaster, id_file,))
runner.invoke_all_and_wait()

print 'Execution Time: %.2fs' % (time() - ts)