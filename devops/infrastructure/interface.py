#!/usr/bin/python
import abc

# ============================================================================ #
# Agnostic of Cloud Service Provider
# ============================================================================ #
class Infrastructure(object):
    __metaclass__ = abc.ABCMeta
    
    # =-=-=--=---=-----=--------=-------------=
    # Settings
    # ----------------------------------------=
    __list_cmd = {
        'update': [
            'sudo apt update -y',
            'sudo apt upgrade -y',
        ],
        'saltmaster': [
        ],
        'cowsay': [
            'sudo apt install cowsay -y',
            'cowsay "William is the Coolest!!"'
        ],
    }
    __recipe = {
        'saltmaster': ['update', 'saltmaster', 'cowsay'],
    }
        
    # =-=-=--=---=-----=--------=-------------=
    # Functions
    # ----------------------------------------=
    def __init__(self):
        self.recipe_saltmaster = self.__get_recipe('saltmaster')
    
    @abc.abstractmethod
    def create_server():
        """
        Spin up a vanilla Linux instance
        """
        return """ @returns HOST on success, False on failure """
    
    @abc.abstractmethod
    def remove_server():
        """
        Destroy a specified Linux instance
            :param KEY - id of machine to delete cleanly
        """
        return """ @returns True on success, False on failure """
    
    # =-=-=--=---=-----=--------=-------------=
    # Helpers
    # ----------------------------------------=
    def __get_recipe(self, recipe_name):
        _return = []
        for key in self.__recipe[recipe_name]:
            _return += self.__list_cmd[key]
        return _return