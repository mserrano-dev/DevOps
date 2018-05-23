# =-=-=--=---=-----=--------=-------------=
# Apply docker-related salt state file
# ----------------------------------------=

{% set args = data['data'] %}

run__docker:
  local.state.sls:
    - name: Run docker container
    - tgt: {{ data['id'] }}
    - arg:
      - docker__{{ args['docker__obj'] }}
