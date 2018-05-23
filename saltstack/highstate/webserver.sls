{% set env = salt.pillar.get('environment') %}

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

mserrano/webserver/install_dependencies/complete:
  event.send:
    - docker__obj: apache2
    - require:
      - pip: docker
