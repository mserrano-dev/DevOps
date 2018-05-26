# =-=-=--=---=-----=--------=-------------=
# HIGHSTATE
# ----------------------------------------=

base:
  'roles:webserver':
    - match: grain
    - webserver.build_dependencies
  'roles:loadbalancer':
    - match: grain
    - loadbalancer.haproxy
