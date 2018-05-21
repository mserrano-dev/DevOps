python-pip:
  pkg:
    - installed

docker:
  pip.installed:
    - name: docker == 3.3.0
    - require:
      - pkg: python-pip

/media/STAGE/webserver/dockerfile:
  file.managed:
    - source: salt://workspace/webserver/dockerfile
    - user: www-data
    - group: www-data
    
/media/STAGE/webserver/.dockerignore:
  file.managed:
    - source: salt://workspace/webserver/.dockerignore
    - user: www-data
    - group: www-data

{% for app, enabled in pillar.get('apps', {}).items() %}
{% if enabled == True %}
/media/STAGE/webserver/{{app}}:
  file.recurse:
    - source: salt://workspace/webserver/{{app}}
    - user: www-data
    - group: www-data
{% endif %}
{% endfor %}
