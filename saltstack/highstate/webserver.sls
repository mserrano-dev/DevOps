python-pip:
  pkg:
    - installed

docker:
  pip.installed:
    - name: docker == 3.3.0
    - require:
      - pkg: python-pip

/media/STAGE/dockerfile:
  file.managed:
    - source: salt://workspace/webserver/dockerfile
    
/media/STAGE/.dockerignore:
  file.managed:
    - source: salt://workspace/webserver/.dockerignore

/media/STAGE/sites: file.directory
    
{% for app, enabled in pillar.get('apps', {}).items() %}
{% if enabled == True %}
/media/STAGE/sites/{{app}}.conf:
  file.managed:
    - source: salt://workspace/sites/{{app}}.conf
    - require:
      - file: /media/STAGE/sites
      
/media/STAGE/webserver/{{app}}:
  file.recurse:
    - source: salt://workspace/webserver/{{app}}
{% endif %}
{% endfor %}
