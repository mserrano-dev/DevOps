# =-=-=--=---=-----=--------=-------------=
# Setup this minion as haproxy server
# ----------------------------------------=

mserrano/loadbalancer/setup/begin:
  event.send:
    - require_in:
      - pkg: build_dependencies
    # ------------------------------------
    # reactor/log__mserrano.sls
    - status: haproxy started
    - comment: installing haproxy dependencies [haproxy]
    # ------------------------------------

/etc/default: file.directory
/etc/haproxy: file.directory

/etc/hosts:
  file.managed:
    - source: salt://workspace/haproxy/hosts

/etc/default/haproxy:
  file.managed:
    - source: salt://workspace/haproxy/haproxy
    - require:
      - file: /etc/default

/etc/haproxy/haproxy.cfg:
  file.managed:
    - source: salt://workspace/haproxy/haproxy.cfg
    - require:
      - file: /etc/haproxy

build_dependencies:
  pkg.installed:
    - pkgs:
      - haproxy
    - require:
      - file: /etc/hosts
      - file: /etc/default/haproxy
      - file: /etc/haproxy/haproxy.cfg

haproxy:
  service.running:
    - enable: True
    - reload: True
    - require:
      - pkg: build_dependencies

mserrano/loadbalancer/setup/complete:
  event.send:
    - require:
      - service: haproxy
    # ------------------------------------
    # reactor/log__mserrano.sls
    - status: haproxy running
    - comment: minion has been setup as haproxy server (haproxy service is running)
    # ------------------------------------
