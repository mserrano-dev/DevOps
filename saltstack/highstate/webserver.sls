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

{% for app, enabled in pillar.get('apps', {}).items() %}
{% if enabled == 'true' %}
/var/www/{{app}}:
  file.symlink:
    - target: /media/STAGE/webserver/{{project_name}}
    - require:
      - file: /media/STAGE
{% endif %}
{% endfor %}