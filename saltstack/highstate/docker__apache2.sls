{% set env = salt.pillar.get('environment') %}

/media/{{ env }}: file.directory
/media/{{ env }}/sites: file.directory
/media/{{ env }}/webserver: file.directory

/media/{{ env }}/dockerfile:
  file.managed:
    - source: salt://workspace/webserver/dockerfile

/media/{{ env }}/.dockerignore:
  file.managed:
    - source: salt://workspace/webserver/.dockerignore

{% for app, enabled in pillar.get('apps', {}).items() %}
{%     if enabled == True %}

/media/{{ env }}/sites/{{ app }}.conf:
  file.managed:
    - source: salt://workspace/sites/{{ app }}.conf
    - require:
      - file: /media/{{ env }}/sites
    - require_in:
      - docker_image: webserver

/media/{{ env }}/webserver/{{ app }}:
  file.recurse:
    - source: salt://workspace/webserver/{{ app }}
    - require:
      - file: /media/{{ env }}/webserver
    - require_in:
      - docker_image: webserver

{%     endif %}
{% endfor %}

webserver:
  docker_image.present:
    - build: /media/STAGE
    - tag: mserrano
    - force: True
    - dockerfile: dockerfile
    - require:
      - file: /media/{{ env }}/sites
      - file: /media/{{ env }}/webserver
      - file: /media/{{ env }}/dockerfile
      - file: /media/{{ env }}/.dockerignore

run_apache2:
  docker_container.running:
    - image: webserver:mserrano
    - skip_translate: True
    - port_bindings: {'80/tcp': 80}
    - publish_all_ports: True
    - replace: True
    - require:
      - docker_image: webserver

mserrano/webserver/setup_apache2_via_docker/complete:
  event.send:
    - status: minion running
    - comment: apache2 is running successfully
    - require:
      - docker_container: run_apache2
