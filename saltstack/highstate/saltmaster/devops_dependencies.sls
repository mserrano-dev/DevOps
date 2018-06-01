# =-=-=--=---=-----=--------=-------------=
# Install pip and pipenv
# ----------------------------------------=

devops_dependencies:
  pkg.installed:
    - pkgs:
      - python-pip

pipenv:
  pip.installed:
    - name: pipenv == 2018.5.18
    - require:
      - pkg: devops_dependencies

cd /media/Devops && pipenv install:
  cmd.run:
    - require:
      - pip: pipenv
