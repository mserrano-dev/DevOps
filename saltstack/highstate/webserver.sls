python-pip:
  pkg:
    - installed

docker:
  pip.installed:
    - name: docker == 3.3.0
    - require:
      - pkg: python-pip

/media/STAGE:
  file.recurse:
    - source: salt://workspace
    - user: www-data
    - group: www-data
    
/var/www:
  file.directory:
    - user: www-data
    - group: www-data

{% for app, enabled in pillar.get('apps', {}).items() %}
{% if enabled == True %}
/var/www/{{app}}:
  file.symlink:
    - target: /media/STAGE/webserver/{{app}}
    - require:
      - file: /media/STAGE
{% endif %}
{% endfor %}
