#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_resourcemanager_project_info
description:
- Gather info for GCP Project
short_description: Gather info for GCP Project
version_added: '2.8'
author: Google Inc. (@googlecloudplatform)
requirements:
- python >= 2.6
- requests >= 2.18.4
- google-auth >= 1.3.0
options:
  project:
    description:
    - The Google Cloud Platform project to use.
    type: str
  auth_kind:
    description:
    - The type of credential used.
    type: str
    required: true
    choices:
    - application
    - machineaccount
    - serviceaccount
  service_account_contents:
    description:
    - The contents of a Service Account JSON file, either in a dictionary or as a
      JSON string that represents it.
    type: jsonarg
  service_account_file:
    description:
    - The path of a Service Account JSON file if serviceaccount is selected as type.
    type: path
  service_account_email:
    description:
    - An optional service account email address if machineaccount is selected and
      the user does not wish to use the default email.
    type: str
  scopes:
    description:
    - Array of scopes to be used
    type: list
  env_type:
    description:
    - Specifies which Ansible environment you're running this module within.
    - This should not be set unless you know what you're doing.
    - This only alters the User Agent string for any API requests.
    type: str
notes:
- for authentication, you can set service_account_file using the c(gcp_service_account_file)
  env variable.
- for authentication, you can set service_account_contents using the c(GCP_SERVICE_ACCOUNT_CONTENTS)
  env variable.
- For authentication, you can set service_account_email using the C(GCP_SERVICE_ACCOUNT_EMAIL)
  env variable.
- For authentication, you can set auth_kind using the C(GCP_AUTH_KIND) env variable.
- For authentication, you can set scopes using the C(GCP_SCOPES) env variable.
- Environment variables values will only be used if the playbook values are not set.
- The I(service_account_email) and I(service_account_file) options are mutually exclusive.
'''

EXAMPLES = '''
- name: get info on a project
  gcp_resourcemanager_project_info:
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
'''

RETURN = '''
resources:
  description: List of resources
  returned: always
  type: complex
  contains:
    number:
      description:
      - Number uniquely identifying the project.
      returned: success
      type: int
    lifecycleState:
      description:
      - The Project lifecycle state.
      returned: success
      type: str
    name:
      description:
      - 'The user-assigned display name of the Project. It must be 4 to 30 characters.
        Allowed characters are: lowercase and uppercase letters, numbers, hyphen,
        single-quote, double-quote, space, and exclamation point.'
      returned: success
      type: str
    createTime:
      description:
      - Time of creation.
      returned: success
      type: str
    labels:
      description:
      - The labels associated with this Project.
      - 'Label keys must be between 1 and 63 characters long and must conform to the
        following regular expression: `[a-z]([-a-z0-9]*[a-z0-9])?`.'
      - Label values must be between 0 and 63 characters long and must conform to
        the regular expression `([a-z]([-a-z0-9]*[a-z0-9])?)?`.
      - No more than 256 labels can be associated with a given resource.
      - Clients should store labels in a representation such as JSON that does not
        depend on specific characters being disallowed .
      returned: success
      type: dict
    parent:
      description:
      - A parent organization.
      returned: success
      type: complex
      contains:
        type:
          description:
          - Must be organization.
          returned: success
          type: str
        id:
          description:
          - Id of the organization.
          returned: success
          type: str
    id:
      description:
      - The unique, user-assigned ID of the Project. It must be 6 to 30 lowercase
        letters, digits, or hyphens. It must start with a letter.
      - Trailing hyphens are prohibited.
      returned: success
      type: str
'''

################################################################################
# Imports
################################################################################
from ansible.module_utils.gcp_utils import navigate_hash, GcpSession, GcpModule, GcpRequest
import json

################################################################################
# Main
################################################################################


def main():
    module = GcpModule(argument_spec=dict())

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/cloud-platform']

    return_value = {'resources': fetch_list(module, collection(module))}
    module.exit_json(**return_value)


def collection(module):
    return "https://cloudresourcemanager.googleapis.com/v1/projects".format(**module.params)


def fetch_list(module, link):
    auth = GcpSession(module, 'resourcemanager')
    return auth.list(link, return_if_object, array_name='projects')


def return_if_object(module, response):
    # If not found, return nothing.
    if response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError) as inst:
        module.fail_json(msg="Invalid JSON response with error: %s" % inst)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))

    return result


if __name__ == "__main__":
    main()
