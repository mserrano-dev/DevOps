# =-=-=--=---=-----=--------=-------------=
# Install docker.io and docker-py
#   then notify to run_docker_apache2
# ----------------------------------------=

mserrano/webserver/install_docker_server/begin:
  event.send:
    - status: minion started
    - comment: installing docker dependencies [docker.io, python-pip]
    - require_in:
      - pkg: build_dependencies

build_dependencies:
  pkg.installed:
    - pkgs:
      - python-pip
      - docker.io

docker:
    pip.installed:
    - name: docker == 3.3.0
    - require:
      - pkg: build_dependencies

mserrano/webserver/install_docker_server/complete:
  event.send:
    - docker__obj: apache2
    - status: minion setup
    - comment: minion has been setup as docker server (docker daemon is running)
    - require:
      - pip: docker
