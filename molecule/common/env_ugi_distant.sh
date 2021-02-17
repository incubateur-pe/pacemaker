REMOTE_HOST=true
CENTOS_BASE_MIRROR=http://10.0.4.40:8081/repository/centos-base/centos
PROVIDER_ARGS=['host="kvm"', 'username="libvirt-user"']
SSH_CONFIG=ssh_config_ugi
SSH_ARGS=-o ProxyCommand="ssh -W %h:%p -q -l libvirt-user kvm"
