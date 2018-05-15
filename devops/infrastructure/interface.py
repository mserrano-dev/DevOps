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
        'update': [
            'sudo apt-get update -y',
            'sudo apt-get upgrade -y',
        ],
        'sleep': [
            'sleep 2',
        ],
        'saltstack': [
            'sudo apt-get install salt-api salt-cloud salt-ssh salt-syndic -y',
        ],
        'master': [
            'sudo apt-get install salt-master -y',
        ],
        'minion': [
            'sudo apt-get install salt-minion -y',
        ],
        'setup_webserver': [
            'sudo salt-key --list-all',
            'sudo salt-key --accept-all -y',
            'sleep 30',
            "sudo salt '*' cmd.run 'sudo apt-get install cowsay -y'",
            "sudo salt '*' cmd.run '/usr/games/cowsay \"William is the Coolest!!\"'",
        ]
    }
    __recipe = {
        'saltstack_master': ['update', 'saltstack', 'master'],
        'saltstack_minion': ['update', 'saltstack', 'minion'],
        'configure_minion': ['sleep', '__minion_config()'],
        'setup_webserver': ['sleep', 'setup_webserver'],
    }
        
    # =-=-=--=---=-----=--------=-------------=
    # Functions
    # ----------------------------------------=
    def __init__(self):
        pass
    
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
    def minion_config(self):
        _return = ["sudo bash -c \"echo master: >> /etc/salt/minion\""]
        for ip_saltmaster in self.list_saltmaster:
            _return.append("sudo bash -c \"echo \ \ - " + ip_saltmaster + " >> /etc/salt/minion\"")
        _return.append("sudo service salt-minion restart")
        
        return _return
    
    def recipe(self, recipe_name):
        _return = []
        for key in self.__recipe[recipe_name]:
            if key in self.__list_cmd:
                _return += self.__list_cmd[key]
            else:
                dynamic_cmd = key.lstrip('_').rstrip('()')
                _return += getattr(self, dynamic_cmd)()
        return _return