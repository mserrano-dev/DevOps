# =-=-=--=---=-----=--------=-------------=
# Install docker.io and docker-py
#   then notify to run_docker_apache2
# ----------------------------------------=

mserrano/webserver/install_docker_server/begin:
  event.send:
    - require_in:
      - pkg: build_dependencies
    # ------------------------------------
    # reactor/log__mserrano.sls
    - status: minion started
    - comment: installing docker dependencies [docker.io, python-pip]
    # ------------------------------------

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
    - require:
      - pip: docker
    # ------------------------------------
    # reactor/run__docker.sls
    - run__docker:
        role: webserver
        container: apache2
    # ------------------------------------
    # reactor/log__mserrano.sls
    - status: minion setup
    - comment: minion has been setup as docker server (docker daemon is running)
    # ------------------------------------
