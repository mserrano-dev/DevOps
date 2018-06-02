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
    log_location_on_remote = '/tmp/mserrano.log' #absolute
    log_location_on_local = '/tmp/mserrano.log' #relative to project root
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
            "sudo apt-get install -y salt-api salt-minion salt-master",
        ],
        "install_as_minion": [
            "sudo apt-get install -y salt-api salt-minion",
        ],
        "setup_master_filesystem": [
            # DevOps
            "sudo git clone https://github.com/mserrano-dev/DevOps.git /media/DevOps/",
            "sudo mkdir -p /srv/projects/workspace/apache2",
            "sudo mkdir -p /srv/projects/workspace/haproxy",
            "sudo ln -s /media/DevOps/bin /srv/projects/workspace/bin",
            "sudo ln -s /media/DevOps/devops /srv/projects/workspace/devops",
            # SaltStack
            "touch %s" % log_location_on_remote,
            "sudo ln -s /media/DevOps/saltstack/highstate /srv/salt",
            "sudo ln -s /media/DevOps/saltstack/grains /srv/salt/_grains",
            "sudo ln -s /media/DevOps/saltstack/pillar /srv/pillar",
            "sudo ln -s /media/DevOps/saltstack/reactor /srv/reactor",
            # Docker
            "sudo ln -s /media/DevOps/docker/apache2/Dockerfile /srv/projects/workspace/apache2/Dockerfile",
            "sudo ln -s /media/DevOps/docker/apache2/.dockerignore /srv/projects/workspace/apache2/.dockerignore",
            # Apache2
            "sudo git clone https://github.com/mserrano-dev/Configuration.git /media/Configuration",
            "sudo ln -s /media/Configuration/apache/sites /srv/projects/workspace/sites",
        ],
        "accept_minions": [
            "sudo cp /media/DevOps/saltstack/settings/master.yml /etc/salt/master",
            wait_until_complete("sudo pkill salt-master"),
            "sudo salt-master -d",
        ],
    }
    
    def do_minion_config_base(self, minion_id, settings_file):
        config = SingleLineFile()
        config.add_line("master:")
        for ip_saltmaster in self.list_saltmaster: # add each saltmaster's IP
            config.add_line("  - " + ip_saltmaster)
        if minion_id != None: # add minion id, if non-None
            config.add_line("id: %s" % minion_id)
        config.append_file(project_fs.read_file(settings_file)) # append the .yml file
        
        _return = []
        _return.append("sudo bash -c \"printf '%s' >> /etc/salt/minion\"" % config.get_file())
        _return.append("sudo service salt-minion restart")
        _return.append("sudo service salt-minion status")
        
        return _return
    
    def do_master_as_minion_config(self):
        return self.do_minion_config_base('master', 'saltstack/settings/master_as_minion.yml')
    
    def do_minion_config(self):
        self.__count_webserver += 1
        webserver_id = "mserrano.webserver-%s" % self.__count_webserver; webserver_id = None
        return self.do_minion_config_base(webserver_id, 'saltstack/settings/minion.yml')
    
    def do_haproxy_config(self):
        # configure the /etc/hosts file
        etc_hosts = SingleLineFile()
        etc_hosts.add_line("%s mserrano.loadbalancer" % self.ip_haproxy)
        for idx, ip_webserver in enumerate(self.list_webserver):
            etc_hosts.add_line("%s mserrano.webserver-%s" % (ip_webserver, idx))
        etc_hosts.add_line("")
        
        # configure the /etc/default/haproxy file
        set_enabled = 'ENABLED=1\n'
        
        # configure the /etc/haproxy/haproxy.cfg file
        haproxy_cfg = project_fs.read_file('saltstack/settings/haproxy.cfg')
        etc_haproxy_cfg = SingleLineFile()
        etc_haproxy_cfg.append_file(haproxy_cfg)
        for idx, ip_webserver in enumerate(self.list_webserver):
            etc_haproxy_cfg.add_line("    server mserrano.webserver-%s  %s:80 maxconn 32" % (idx, ip_webserver))
        etc_haproxy_cfg.add_line("")
        
        _return = []
        _return.append("sudo bash -c \"printf '%s' >> /srv/projects/workspace/haproxy/hosts\"" % etc_hosts.get_file())
        _return.append("sudo bash -c \"printf '%s' >> /srv/projects/workspace/haproxy/haproxy\"" % set_enabled)
        _return.append("sudo bash -c \"printf '%s' >> /srv/projects/workspace/haproxy/haproxy.cfg\"" % etc_haproxy_cfg.get_file())
        
        return _return
    
    # =-=-=--=---=-----=--------=-------------=
    # Functions
    # ----------------------------------------=
    def __init__(self):
        self.__count_webserver = 0
        self.__recipe = {
            'saltstack_master': ['update_saltstack', 'install_as_master'],
            'saltstack_minion': ['update_saltstack', 'install_as_minion'],
            'configure_minion': ['sleep', '__do_minion_config()'],
            'configure_master_as_minion': ['_do_master_as_minion_config()'],
            'configure_master': [
                'setup_master_filesystem',
                '__do_haproxy_config()',
                'accept_minions',
            ],
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
