# =-=-=--=---=-----=--------=-------------=
# Install pip packages from
#   pipenv generated requirements.txt
# ----------------------------------------=

devops_dependencies:
  pkg.installed:
    - pkgs:
      - python-pip

pip-install-requirements:
  pip.installed:
    - requirements:
      - /media/DevOps/requirements.txt
    - require:
      - pkg: devops_dependencies
