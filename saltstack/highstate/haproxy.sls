# =-=-=--=---=-----=--------=-------------=
# Setup this minion as haproxy server
# ----------------------------------------=

mserrano/haproxy/setup/begin:
  event.send:
    - status: haproxy started
    - comment: installing haproxy dependencies [haproxy]
    - require_in:
      - pkg: build_dependencies

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

mserrano/haproxy/setup/complete:
  event.send:
    - docker__obj: apache2
    - status: haproxy running
    - comment: minion has been setup as haproxy server (haproxy service is running)
    - require:
      - service: haproxy
