{% set args = data['data'] %}
{% set log_file = '/tmp/mserrano.log' %}
{% set minion_id =  data['id'] %}
{% set timestamp = '' %}

log__banner:
  local.cmd.run:
    - comment: present standard info 
    - tgt: 'master*'
    - arg:
      - 'printf "[{{ minion_id }}] [{{ args['status'] }}] - ({{ tag }})\n" >> {{ log_file }}'

log__entry:
  local.cmd.run:
    - comment: timestamped comment with end banner
    - tgt: 'master*'
    - arg:
      - 'printf "[{{ timestamp }}] {{ args['comment'] }}\n---\n" >> {{ log_file }}'
