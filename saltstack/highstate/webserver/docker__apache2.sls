# =-=-=--=---=-----=--------=-------------=
# Setup a running docker container
#   apache2 via port 80
# ----------------------------------------=

{% set env = salt.pillar.get('environment') %}
{% set default_app = salt.pillar.get('default_app') %}

/media/{{ env }}: file.directory
/media/{{ env }}/sites: file.directory
/media/{{ env }}/apache2: file.directory

/media/{{ env }}/Dockerfile:
  file.managed:
    - source: salt://workspace/apache2/Dockerfile

/media/{{ env }}/.dockerignore:
  file.managed:
    - source: salt://workspace/apache2/.dockerignore

{% for git_repo, conf in pillar.get('apps', {}).items() %}
{%     if conf != None %}

/media/{{ env }}/sites/{{ conf }}.conf:
  file.managed:
    - source: salt://workspace/sites/{{ conf }}.conf
    - require:
      - file: /media/{{ env }}/sites
    - require_in:
      - docker_image: webserver

clone-{{ git_repo }}:
  git.latest:
    - name: https://github.com/mserrano-dev/{{ git_repo }}.git
    - target: /media/{{ env }}/apache2/{{ conf }}
    - branch: {{ env }}
    - require_in:
      - docker_image: webserver

{%     endif %}
{% endfor %}

/media/{{ env }}/sites/000-default.conf:
  file.managed:
    - source: salt://workspace/sites/{{ default_app }}.conf
    - require:
      - file: /media/{{ env }}/sites
    - require_in:
      - docker_image: webserver

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
