#!/usr/bin/python
from abc import *
from util import project_fs
from util.bash_arg import *

# ============================================================================ #
# Agnostic of Cloud Service Provider
# ============================================================================ #
class Infrastructure(object):
    __metaclass__ = ABCMeta
    
    # =-=-=--=---=-----=--------=-------------=
    # Settings
    # ----------------------------------------=
    __list_cmd = {
        "sleep": [
            "sleep 2",
        ],
        "update_saltstack": [
            "wget -O - https://repo.saltstack.com/apt/debian/9/amd64/archive/2018.3.0/SALTSTACK-GPG-KEY.pub | sudo apt-key add -",
            "sudo bash -c \"printf 'deb http://repo.saltstack.com/apt/debian/9/amd64/archive/2018.3.0 stretch main' >> /etc/apt/sources.list.d/saltstack.list\"",
            "sudo apt-get update -y",
        ],
        "install_as_master": [
            "sudo apt-get install -y salt-api salt-syndic salt-master",
        ],
        "install_as_minion": [
            "sudo apt-get install -y salt-api salt-syndic salt-minion",
        ],
        "setup_master_filesystem": [
            # DevOps
            "sudo git clone https://github.com/mserrano-dev/DevOps.git /media/DevOps/",
            "sudo mkdir -p /srv/projects/workspace/webserver",
            "sudo ln -s /media/DevOps/bin /srv/projects/workspace/bin",
            "sudo ln -s /media/DevOps/devops /srv/projects/workspace/devops",
            # SaltStack
            "sudo ln -sf /media/DevOps/saltstack/highstate /srv/salt",
            "sudo ln -sf /media/DevOps/saltstack/pillar /srv/pillar",
            # Docker
            "sudo ln -s /media/DevOps/docker/dockerfile /srv/projects/workspace/webserver/dockerfile",
            "sudo ln -s /media/DevOps/docker/.dockerignore /srv/projects/workspace/webserver/.dockerignore",
            # Apache2
            "sudo git clone https://github.com/mserrano-dev/Configuration.git /media/Configuration",
            "sudo ln -s /media/Configuration/apache/sites /srv/projects/workspace/sites",
            # WebServer
            "sudo git clone https://github.com/mserrano-dev/LAB-MSERRANO.git /srv/projects/workspace/webserver/LAB.NET",
            "sudo git clone https://github.com/mserrano-dev/WS-MSERRANO.git /srv/projects/workspace/webserver/WS.NET",
            "sudo git clone https://github.com/mserrano-dev/WWW-MSERRANO.git /srv/projects/workspace/webserver/WWW.NET",
            "sudo git clone https://github.com/mserrano-dev/DOCS-MSERRANO.git /srv/projects/workspace/webserver/DOCS.NET",
        ],
        "accept_minions": [
            "sudo cp /media/DevOps/saltstack/settings/master.yml /etc/salt/master",
            "while sudo pkill salt-master; do sleep 0.2; done",
            wait_until_complete("sudo pkill salt-master"),
            "sudo salt-master -d",
        ],
    }
    
    def do_minion_config(self):
        config = SingleLineFile()
        config.add_line("master:")
        for ip_saltmaster in self.list_saltmaster: # add each saltmaster's IP
            config.add_line("  - " + ip_saltmaster)
        config.append_yaml_file(project_fs.read_file('saltstack/settings/minion.yml')) # append the minion.yml file

        _return = []
        _return.append("sudo bash -c \"printf '%s' >> /etc/salt/minion\"" % config.get_file())
        _return.append("sudo service salt-minion restart")
        _return.append("sudo service salt-minion status") 
        
        return _return
    
    # =-=-=--=---=-----=--------=-------------=
    # Functions
    # ----------------------------------------=
    def __init__(self):
        self.__recipe = {
            'saltstack_master': ['update_saltstack', 'install_as_master'],
            'saltstack_minion': ['update_saltstack', 'install_as_minion'],
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