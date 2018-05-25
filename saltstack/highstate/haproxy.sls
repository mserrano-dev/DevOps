# =-=-=--=---=-----=--------=-------------=
# Setup this minion as haproxy server
# ----------------------------------------=

mserrano/haproxy/setup/begin:
  event.send:
    - status: haproxy started
    - comment: installing haproxy dependencies [haproxy]
    - require_in:
      - pkg: build_dependencies

build_dependencies:
  pkg.installed:
    - pkgs:
      - haproxy

mserrano/haproxy/setup/complete:
  event.send:
    - docker__obj: apache2
    - status: haproxy running
    - comment: minion has been setup as haproxy server (haproxy service is running)
    - require:
      - pkg: build_dependencies
