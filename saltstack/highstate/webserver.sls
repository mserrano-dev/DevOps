{% set env = salt.pillar.get('environment') %}

python-pip:
  pkg:
    - installed

docker:
  pip.installed:
    - name: docker == 3.3.0
    - require:
      - pkg: python-pip

/media/{{ env }}/dockerfile:
  file.managed:
    - source: salt://workspace/webserver/dockerfile

/media/{{ env }}/.dockerignore:
  file.managed:
    - source: salt://workspace/webserver/.dockerignore

/media/{{ env }}/sites: file.directory

{% for app, enabled in pillar.get('apps', {}).items() %}
{% if enabled == True %}
/media/{{ env }}/sites/{{ app }}.conf:
  file.managed:
    - source: salt://workspace/sites/{{ app }}.conf
    - require:
      - file: /media/{{ env }}/sites

/media/{{ env }}/webserver/{{ app }}:
  file.recurse:
    - source: salt://workspace/webserver/{{ app }}
{% endif %}
{% endfor %}
