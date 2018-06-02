# DevOps  
<p align="left">
    <img src="https://avatars2.githubusercontent.com/u/30729323?s=200&v=4" title="mserrano-dev (DevOps)"></img>
</p>  

__SaltStack + Docker + Apache2 + HAProxy + Python + Bash__  
Continuous Integration Tools and Configuration Management via Infrastructure as Code

---
__New Dev?__
##### install python dependencies
```shell
apt install pip
pip install pipenv
cd DevOps
pipenv install
```

##### deploy an mserrano.net app
```shell
cd DevOps/bin
./deploy <git_repo>
```

##### re-launch mserrano.net entirely
```shell
cd DevOps/bin
./restart_infrastructure
```

__Trouble-shooter__
##### WARNING: POSSIBLE DNS SPOOFING DETECTED!
its ok, the domain mserrano.net is probably pointing to a new machine. Most likely a fellow mserrano-dev triggered  
script ./restart_infrastructure. This causes Route53 to update our *.mserrano.net dns record to point to the new saltmaster/loadbalancer server.

##### remove old host key & add new one
```shell
cd DevOps/bin
./update_knownhosts
```
