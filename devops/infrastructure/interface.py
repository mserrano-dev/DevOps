#!/usr/bin/python
from abc import *

# ============================================================================ #
# Agnostic of Cloud Service Provider
# ============================================================================ #
class Infrastructure(object):
    __metaclass__ = ABCMeta
    
    # =-=-=--=---=-----=--------=-------------=
    # Settings
    # ----------------------------------------=
    __list_cmd = {
        "update": [
            "sudo apt-get update -y",
            "sudo apt-get upgrade -y",
        ],
        "sleep": [
            "sleep 2",
        ],
        "saltstack": [
            "sudo apt-get install salt-api salt-cloud salt-ssh salt-syndic -y",
        ],
        "install_as_master": [
            "sudo apt-get install salt-master -y",
        ],
        "install_as_minion": [
            "sudo apt-get install salt-minion -y",
        ],
        "accept_minions": [
            "sudo bash -c 'echo auto_accept: True >> /etc/salt/master'",
            "sudo pkill salt-master",
            "sudo salt-master -d",
        ],
        "setup_minion_filesystem": [
            "sudo salt '*' cmd.run 'sudo mkdir -p /media/DEV/workspace/'",
            "sudo salt '*' cmd.run 'sudo mkdir -p /var/www/'",
            "sudo salt '*' git.clone /media/DEV/workspace/DevOps https://github.com/mserrano-dev/DevOps.git",
            "sudo salt '*' git.clone /media/DEV/workspace/LAB-MSERRANO https://github.com/mserrano-dev/LAB-MSERRANO.git",
            "sudo salt '*' cmd.run 'sudo chown -R www-data:www-data /media/DEV/workspace'",
            "sudo salt '*' cmd.run 'sudo ln -s /media/DEV/workspace/LAB-MSERRANO/ /var/www/LAB.NET'",
        ],
    }
    
    def do_minion_config(self):
        _return = ["sudo bash -c \"echo master: >> /etc/salt/minion\""]
        for ip_saltmaster in self.list_saltmaster:
            _return.append("sudo bash -c \"echo \ \ - " + ip_saltmaster + " >> /etc/salt/minion\"")
        _return.append("sudo service salt-minion restart")
        _return.append("sudo service salt-minion status")
        
        return _return
    
    # =-=-=--=---=-----=--------=-------------=
    # Functions
    # ----------------------------------------=
    def __init__(self):
        self.__recipe = {
            'saltstack_master': ['update', 'saltstack', 'install_as_master'],
            'saltstack_minion': ['update', 'saltstack', 'install_as_minion'],
            'configure_minion': ['sleep', '__do_minion_config()'],
            'setup_webserver': ['accept_minions', 'setup_minion_filesystem'],
        }
    
    @abstractmethod
    def create_server(self):
        """
        Spin up a vanilla Linux instance
            :param COUNT - number of instances to spin up
        """
        return """ @returns []<dict> on success,
                            <bool>False on failure """
    
    @abstractmethod
    def collect_info(self):
        """
        Collect information about a Linux instance
            :param OBJ - instance to get info from
        """
        return """ @returns <dict>{KEY:<string>,
                                   HOST:<string>,
                                   IP:<string>} on success,
                            <bool>False on failure """
    
    @abstractmethod
    def remove_server(self):
        """
        Destroy a specified Linux instance
            :param KEY - list or string, of instance(s) to be terminated
        """
        return """ @returns <bool>True on success, 
                            <bool>False on failure """
                            
    # =-=-=--=---=-----=--------=-------------=
    # Helpers
    # ----------------------------------------=
    def recipe(self, recipe_name):
        _return = []
        for key in self.__recipe[recipe_name]:
            if key in self.__list_cmd:
                _return += self.__list_cmd[key]
            else:
                dynamic_cmd = key.lstrip('_').rstrip('()')
                _return += getattr(self, dynamic_cmd)()
        return _return