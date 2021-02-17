REMOTE_HOST=true
CENTOS_BASE_MIRROR=https://repository.pole-emploi.intra/artifactory/rpm-base-centos-proxy
PROVIDER_ARGS=['host="iugi3000-HP-ProDesk-400-G4-MT.dgasi.pole-emploi.intra"', 'username="libvirt-user"']
SSH_CONFIG=ssh_config_pe
SSH_ARGS=-o ProxyCommand="ssh -W %h:%p -q -l libvirt-user iugi3000-HP-ProDesk-400-G4-MT.dgasi.pole-emploi.intra"
http_proxy
https_proxy
HTTP_PROXY
HTTPS_PROXY
no_proxy
NO_PROXY
