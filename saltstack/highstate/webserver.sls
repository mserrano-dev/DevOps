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

/media/{{ env }}: file.directory

/media/{{ env }}/sites: file.directory

/media/{{ env }}/dockerfile:
  file.managed:
    - source: salt://workspace/webserver/dockerfile
    - require:
      - file: /media/{{ env }}

/media/{{ env }}/.dockerignore:
  file.managed:
    - source: salt://workspace/webserver/.dockerignore
    - require:
      - file: /media/{{ env }}

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
