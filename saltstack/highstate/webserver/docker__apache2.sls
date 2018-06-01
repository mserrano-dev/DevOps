# =-=-=--=---=-----=--------=-------------=
# Setup a running docker container
#   apache2 via port 80
# ----------------------------------------=

{% set env = salt.pillar.get('environment') %}

/media/{{ env }}: file.directory
/media/{{ env }}/sites: file.directory
/media/{{ env }}/apache2: file.directory

/media/{{ env }}/Dockerfile:
  file.managed:
    - source: salt://workspace/apache2/Dockerfile

/media/{{ env }}/.dockerignore:
  file.managed:
    - source: salt://workspace/apache2/.dockerignore

{% for app, enabled in pillar.get('apps', {}).items() %}
{%     if enabled == True %}

/media/{{ env }}/sites/{{ app }}.conf:
  file.managed:
    - source: salt://workspace/sites/{{ app }}.conf
    - require:
      - file: /media/{{ env }}/sites
    - require_in:
      - docker_image: webserver

/media/{{ env }}/apache2/{{ app }}:
  file.recurse:
    - source: salt://workspace/apache2/{{ app }}
    - require:
      - file: /media/{{ env }}/apache2
    - require_in:
      - docker_image: webserver

{%     endif %}
{% endfor %}

webserver:
  docker_image.present:
    - build: /media/{{ env }}
    - tag: mserrano
    - force: True
    - require:
      - file: /media/{{ env }}/sites
      - file: /media/{{ env }}/apache2
      - file: /media/{{ env }}/Dockerfile
      - file: /media/{{ env }}/.dockerignore

run_apache2:
  docker_container.running:
    - image: webserver:mserrano
    - skip_translate: True
    - port_bindings: {'80/tcp': 80}
    - publish_all_ports: True
    - binds:
      - /media/{{ env }}/apache2:/var/www
      - /media/{{ env }}/sites:/etc/apache2/sites-enabled
    - require:
      - docker_image: webserver

mserrano/webserver/setup_apache2_via_docker/complete:
  event.send:
    - require:
      - docker_container: run_apache2
    # ------------------------------------
    # reactor/log__mserrano.sls
    - status: minion running
    - comment: apache2 is running and ready to serve traffic
    # ------------------------------------
