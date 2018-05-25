# =-=-=--=---=-----=--------=-------------=
# HIGHSTATE
# ----------------------------------------=

base:
  'roles:web':
    - match: grain
    - webserver
  'roles:load_balancer':
    - match: grain
    - haproxy
