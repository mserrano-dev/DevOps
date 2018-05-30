# =-=-=--=---=-----=--------=-------------=
# Verify a correct loadbalancer setup
# ----------------------------------------=

#should-signal-loadbalancer-setup-begin:

should-have-haproxy-installed:
  module_and_function: pkg.list_pkgs
  args: ''
  kwargs: ''
  pillar-data: ''
  assertion: assertIn
  expected-return: 'haproxy'

#should-have-file-etc-hosts:

#should-have-file-etc-default-haproxy:

#should-have-file-etc-haproxy:

#should-have-haproxy-running:

#should-signal-loadbalancer-setup-complete:
