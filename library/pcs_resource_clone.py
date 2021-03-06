#!/usr/bin/python


# Copyright: (c) 2021, Ulrich GIRAUD <ulrich.giraud1@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

import xml.etree.ElementTree as ET
from distutils.spawn import find_executable
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
author: "Ulrich GIRAUD"
module: pcs_resource_clnoe
short_description: "wrapper module for 'pcs resource clone' "
description:
     - "Module for cloning and uncloning resources using 'pcs' utility."
     - "This module should be executed for same resorce only on one of the nodes in cluster at a time."
version_added: "2.4"
options:
  state:
    description:
      - "'present' - ensure that cluster resource is cloned"
      - "'absent' - ensure cluster resource isn't cloned"
    required: false
    default: present
    choices: ['present', 'absent']
    type: str
  name:
    description:
      - "name of cluster resource - cluster resource identifier"
    required: true
    type: str
  options:
    description:
      - "additional options passed to 'pcs' command"
    required: false
    type: str
  force_resource_update:
    description:
      - "skip checking for cluster changes when updating existing resource configuration
        -  use 'scope=resources' when pushing the change to cluster. Useful in busy clusters,
        dangerous when there are concurent updates as they can be lost."
    required: false
    default: no
    type: bool
'''

EXAMPLES = '''
- name: Clone test resource
  pcs_resource_clone:
    name: 'test'

- name: Unclone test resource
  pcs_resource_clone:
    name: 'test'
    state: 'absent'
'''


def find_resource(cib, resource_id):
    my_resource = {"configuration": None, "is_clone": False}
    for elem in list(cib):
        if elem.attrib.get('id') == resource_id:
            return {"configuration": elem, "is_clone": False}
        elif elem.tag == 'clone':
            my_resource = find_resource(elem, resource_id)
            my_resource["is_clone"] = True
            if my_resource is not None:
                break
    return my_resource


def run_module():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default="present", choices=['present', 'absent']),
            name=dict(required=True),
            options=dict(default="", required=False),
            force_resource_update=dict(default=False, type='bool', required=False),
        ),
        supports_check_mode=True
    )

    state = module.params['state']
    resource_name = module.params['name']

    result = {}

    if find_executable('pcs') is None:
        module.fail_json(msg="'pcs' executable not found. Install 'pcs'.")

    # get running cluster configuration
    rc, out, err = module.run_command('pcs cluster cib')
    if rc == 0:
        current_cib_root = ET.fromstring(out)
    else:
        module.fail_json(msg='Failed to load cluster configuration', out=out, error=err)

    # try to find the resource that we seek
    resource = None
    cib_resources = current_cib_root.find('./configuration/resources')
    resource = find_resource(cib_resources, resource_name)

    if resource["configuration"] is None:
        module.fail_json(msg='No resource found to clone')

    if state == 'present' and not resource["is_clone"]:
        # resource should be cloned, but we don't see it in configuration - lets create it
        result['changed'] = True
        if not module.check_mode:
            cmd = 'pcs resource clone %(name)s %(options)s' % module.params
            rc, out, err = module.run_command(cmd)
            if rc != 0 and "Call cib_replace failed (-62): Timer expired" in err:
                # EL6: special retry when we failed to create resource because of timer waiting on cib expired
                rc, out, err = module.run_command(cmd)
            if rc == 0:
                module.exit_json(changed=True)
            else:
                module.fail_json(msg="Failed to clone resource using command '" + cmd + "'", output=out, error=err)

    elif state == 'absent' and resource['is_clone']:
        # resource clone should not be present but we have found something - lets remove that
        result['changed'] = True
        if not module.check_mode:
            cmd = 'pcs resource unclone %(name)s' % module.params
            rc, out, err = module.run_command(cmd)
            if rc == 0:
                module.exit_json(changed=True)
            else:
                module.fail_json(msg="Failed to delete resource using command '" + cmd + "'", output=out, error=err)

    else:
        # resource should not be present and is nto there, nothing to do
        result['changed'] = False

    # END of module
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
