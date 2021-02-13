REMOTE_HOST=true
PROVIDER_ARGS=['host="kvm"', 'username="libvirt-user"']
SSH_CONFIG=ssh_config_ugi
SSH_ARGS=-o ProxyCommand="ssh -W %h:%p -q -l libvirt-user kvm"
