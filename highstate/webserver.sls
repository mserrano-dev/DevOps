python-pip:
  pkg:
    - installed

/var/www:
  file.recurse:
    - source: salt://workspace
    - user: www-data
    - group: www-data