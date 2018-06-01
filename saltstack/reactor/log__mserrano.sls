# =-=-=--=---=-----=--------=-------------=
# Event-driven logging to /tmp directory
# ----------------------------------------=
{% set log_file = '/tmp/mserrano.log' %}

{% set args = data['data'] %}
{% set minion_id =  data['id'] %}
#% set timestamp = None|strftime('%Y-%m-%d %H:%M:%S') %} #TODO on release 2018.3.1
{% set timestamp = salt['cmd.run']('date "+%Y-%m-%d %H:%M:%S"') %} # workaround

log__banner:
  local.cmd.run:
    - comment: present standard info
    - tgt: 'roles:saltmaster'
    - tgt_type: grain
    - arg:
      - 'printf "[{{ minion_id }}] [{{ args['status'] }}] - ({{ tag }})\n" >> {{ log_file }}'

log__entry:
  local.cmd.run:
    - comment: timestamped comment with end banner
    - tgt: 'roles:saltmaster'
    - tgt_type: grain
    - arg:
      - 'printf "[{{ timestamp }}] {{ args['comment'] }}\n---\n" >> {{ log_file }}'
