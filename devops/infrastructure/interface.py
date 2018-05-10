#!/usr/bin/python
import abc

# ---------------------------------------------------------------------------- #
# Agnostic of Cloud Service Provider
# ---------------------------------------------------------------------------- #
class Platform(object):
    __metaclass__ = abc.ABCMeta
    
    recipe_saltmaster = [
        'sudo apt update -y',
        'sudo apt upgrade -y',
        'sudo apt install cowsay -y',
        'cowsay "William is the Coolest!!"'
    ]
    
    @abc.abstractmethod
    def create_server():
        """
        Spin up a vanilla Linux instance
        """
        return """ @returns HOST on success, NULL on failure """
    
    @abc.abstractmethod
    def remove_server():
        """
        Destroy a specified Linux instance
            :param KEY - id of machine to delete cleanly
        """
        return """ @returns NULL """