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
        "setup_master_filesystem": [
            "sudo git clone https://github.com/mserrano-dev/DevOps.git /media/DevOps/",
            "sudo git clone https://github.com/mserrano-dev/LAB-MSERRANO.git /srv/projects/workspace/LAB.NET",
            "sudo git clone https://github.com/mserrano-dev/WS-MSERRANO.git /srv/projects/workspace/WS.NET",
            "sudo git clone https://github.com/mserrano-dev/WWW-MSERRANO.git /srv/projects/workspace/WWW.NET",
            "sudo git clone https://github.com/mserrano-dev/DOCS-MSERRANO.git /srv/projects/workspace/DOCS.NET",
            "sudo ln -s /media/DevOps/highstate /srv/salt",
        ],
        "accept_minions": [
            "sudo cp /media/DevOps/settings/master.yml /etc/salt/master",
            "sudo pkill salt-master",
            "sudo salt-master -d",
        ],
    }
    
    def do_minion_config(self):
        _return = ["sudo bash -c \"echo master: >> /etc/salt/minion\""]
        for ip_saltmaster in self.list_saltmaster:
            _return.append("sudo bash -c \"echo \ \ - " + ip_saltmaster + " >> /etc/salt/minion\"")
        _return.append("sudo bash -c \"echo startup_states: highstate >> /etc/salt/minion\"")
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
            'setup_webserver': ['setup_master_filesystem', 'accept_minions'],
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