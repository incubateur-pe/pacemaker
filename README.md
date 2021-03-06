pacemaker
=========

Install pacemaker and configure High Availability

Role Variables
--------------

|    |     |     |
|----|-----|-----|
| pcs_cluster_user | User for pcs |  pcs_cluster |
| pcs_cluster_user_group | Group to assign the user to | pcs_cluster |
| pcs_cluster_user_pass | password for the cluster | pcs_cluster |
| pcs_cluster_name | Name of the cluster | pcs_cluster |
| pcs_fencing_libvirt_enabled | Configure fencing with libvirt | false |
| pcs_vm_name | Each host in the play should be configured if hostname is different from vm name |  "{{ ansible_hostname }}" |
| pcs_fencing_vmware_enabled | Configure fencing for vmware rest | false |
| pcs_virtual_ips | Virtual IP ressources to add to the cluster | [] |
| pcs_virtual_ips[].name | name of the ressource to configure | N/A |
| pcs_virtual_ips[].ip | ip address to configure | N/A |
| pcs_service_resources | Service resources to add to the cluster | [] |
| pcs_service_resources[].name | name of the service to configure | N/A |
| pcs_service_resources[].prefix | prefix to add to the resource name | N/A |
| pcs_service_resources[].options | resource options | N/A |
| pcs_service_resources[].clone | define the ressource as a clone | N/A |
| pcs_colocations | set up resources colocations | [] |
| pcs_colocations.resource1 | name of the first resource | N/A |
| pcs_colocations.resource2 | name of the second resource | N/A |
| pcs_colocations.ordered | Apply an order constraint when set  | false |
| pcs_stickiness_default | Define a stickiness=100 as resource default | false |
| pcs_prometheus_exporter | Installs a prometheus exporter listening on port 9664 | true |
| pcs_prometheus_exporter_base_url | Base url to download exporter binaries | https://github.com |
| pcs_prometheus_exporter_version | ha_cluster_exporter version to install | 1.2.1 |


Dependencies
------------

  * ondrejhome.pcs-modules-2

Example Playbook
----------------

```
- name: Set up High Availability
  hosts: all
  tasks:
    - name: "Include pacemaker"
      include_role:
        name: "pacemaker"
      vars:
        pcs_fencing_libvirt_enabled: true
        pcs_fencing_libvirt_key: "{{ role_path + '/tests/fence_key' }}"

        pcs_virtual_ips:
          - name: VirtualIP0
            ip: 192.168.121.10
          - name: VirtualIP1
            ip: 192.168.121.20
        
        pcs_service_resources:
          - name: haproxy
            prefix: Service_
            options: op monitor interval=5s

        pcs_colocations:
          - resource1: VirtualIP0
            resource2: Service_haproxy
            ordered: true
          - resource1: VirtualIP1
            resource2: Service_haproxy
            ordered: true
```

License
-------

BSD-3-Clause
