# =-=-=--=---=-----=--------=-------------=
# Update an app to its latest version
# ----------------------------------------=

{% set env = salt.pillar.get('environment') %}
{% set my_app = salt.pillar.get('git_repo') %}

mserrano/webserver/deploy_app/begin:
  event.send:
    - require_in:
      - git: update-{{ my_app }}
    # ------------------------------------
    # reactor/log__mserrano.sls
    - status: {{ my_app }} stale
    - comment: deploying {{ my_app }} to {{ env }}
    # ------------------------------------

{% for git_repo, conf in pillar.get('apps', {}).items() %}
{%     if conf != None %}
{%         if my_app == git_repo %}

update-{{ my_app }}:
  git.latest:
    - name: https://github.com/mserrano-dev/{{ git_repo }}.git
    - target: /media/{{ env }}/apache2/{{ conf }}
    - branch: {{ env }}

{%         endif %}
{%     endif %}
{% endfor %}

mserrano/webserver/deploy_app/complete:
  event.send:
    - require:
      - git: update-{{ my_app }}
    # ------------------------------------
    # reactor/log__mserrano.sls
    - status: {{ my_app }} updated
    - comment: {{ my_app }} deployed successfully
    # ------------------------------------
