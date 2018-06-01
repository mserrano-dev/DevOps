# =-=-=--=---=-----=--------=-------------=
# HIGHSTATE
# ----------------------------------------=

base:
  'roles:saltmaster':
    - match: grain
    - saltmaster.init
  'roles:webserver':
    - match: grain
    - webserver.init
  'roles:loadbalancer':
    - match: grain
    - loadbalancer.init
