python-pip:
  pkg:
    - installed

docker:
  pip.installed:
    - name: docker == 3.3.0
    - require:
      - pkg: python-pip

/var/www:
  file.recurse:
    - source: salt://workspace
    - user: www-data
    - group: www-data