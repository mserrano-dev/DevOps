{% set minion = salt.config.minion_config('/etc/salt/minion') %}

log__new_minion:
  local.cmd.run:
    - name: log new minion
    - tgt: 'master*'
    - arg:
      - 'printf "[{{ minion['id'] }}][minion started] A new Minion has started on $(date). ({{ tag }})\n" >> /tmp/salt.reactor.log'
