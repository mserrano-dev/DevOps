# =-=-=--=---=-----=--------=-------------=
# Apply docker-related salt state file
# ----------------------------------------=

{% set args = data['data'] %}
{% set role = args['run__docker']['role'] %}
{% set container = args['run__docker']['container'] %}

run__docker:
  local.state.sls:
    - name: Run docker container
    - tgt: {{ data['id'] }}
    - arg:
      - {{ role }}.docker__{{ container }}
