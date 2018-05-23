log__new_minion:
  local.cmd.run:
    - name: log new webserver
    - tgt: '*'
    - arg:
      - 'printf "[{{ data['id'] }}][minion started] A new Minion has started on $(date). ({{ tag }})\n" >> /tmp/salt.reactor.log'
