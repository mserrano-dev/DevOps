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
        'cowsay': [
            'sudo apt-get install cowsay -y',
            'cowsay "William is the Coolest!!"',
        ],
        'saltstack': [
            'sudo apt-get install salt-api salt-cloud salt-ssh salt-syndic -y',
        ],
        'saltmaster': [
            'sudo apt-get install salt-master -y',
        ],
        'webserver': [
            'sudo apt-get install salt-minion -y',
        ],
    }
    __recipe = {
        'saltmaster': ['update', 'saltstack', 'saltmaster'],
        'webserver': ['update', 'saltstack', 'webserver'],
    }
        
    # =-=-=--=---=-----=--------=-------------=
    # Functions
    # ----------------------------------------=
    def __init__(self):
        self.recipe_saltmaster = self.__get_recipe('saltmaster')
        self.recipe_webserver = self.__get_recipe('webserver')
    
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
    def __get_recipe(self, recipe_name):
        _return = []
        for key in self.__recipe[recipe_name]:
            _return += self.__list_cmd[key]
        return _return