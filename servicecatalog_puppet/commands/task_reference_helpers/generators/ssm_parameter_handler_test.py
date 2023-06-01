#  Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0

import unittest

from servicecatalog_puppet import constants


class SSMParameterHandlerTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        from servicecatalog_puppet.commands.task_reference_helpers.generators import (
            ssm_parameter_handler,
        )

        self.sut = ssm_parameter_handler

    def test_for_ssm_parameters_for_spoke_execution_mode(self):
        # setup
        puppet_account_id = "hub_account_id"
        account_id = "spoke_account_id"
        region = "eu-west-0"
        default_region = "eu-south-0"
        item_name = "depsrefactor"
        dependency_item_name = "something_else"

        task = {
            "stack_name": item_name,
            "launch_name": "",
            "stack_set_name": "",
            "capabilities": ["CAPABILITY_NAMED_IAM"],
            "ssm_param_outputs": [],
            "bucket": f"sc-puppet-stacks-repository-{puppet_account_id}",
            "key": f"stack/{item_name}/v1/stack.template-${{AWS::Region}}.yaml",
            "version_id": "",
            "execution": "spoke",
            "use_service_role": True,
            "tags": [],
            "puppet_account_id": puppet_account_id,
            "status": None,
            "requested_priority": 0,
            "dependencies": [
                {"affinity": "stack", "name": dependency_item_name, "type": "stack",}
            ],
            "account_id": account_id,
            "region": region,
            "manifest_section_names": {"stacks": True},
            "manifest_item_names": {item_name: True},
            "manifest_account_ids": {account_id: True},
            "section_name": "stacks",
            "item_name": item_name,
            "dependencies_by_reference": [
                "create-policies",
                f"prepare-account-for-stacks-{account_id}",
                f"get-template-from-s3-stacks-{item_name}",
            ],
            "task_reference": f"{account_id}-{region}",
            "get_s3_template_ref": f"get-template-from-s3-stacks-{item_name}",
        }
        task_reference = task["task_reference"]
        all_tasks = {task_reference: task}

        parameter_path = "/sleeper/SleeperFunctionArn/${AWS::Region}/stacks"

        parameter_details = {
            "ssm": {"name": parameter_path, "account_id": "${AWS::AccountId}"}
        }

        # exercise
        self.sut.ssm_parameter_handler(
            all_tasks,
            default_region,
            all_tasks,
            parameter_details,
            puppet_account_id,
            task,
        )

        # verify
        n_all_tasks = len(all_tasks.keys())
        self.assertEqual(
            [
                "create-policies",
                f"prepare-account-for-stacks-{account_id}",
                f"get-template-from-s3-stacks-{item_name}",
                f"{constants.SSM_PARAMETERS}-{account_id}-{default_region}-{f'/sleeper/SleeperFunctionArn/{region}/stacks'}",
            ],
            all_tasks[task_reference].get("dependencies_by_reference"),
            "assert new dependency is added to the task needing the parameter",
        )

        expected_ssm_parameter_task_ref = f"{constants.SSM_PARAMETERS}-{account_id}-{default_region}-{f'/sleeper/SleeperFunctionArn/{region}/stacks'}"
        self.assertEqual(
            {
                "account_id": account_id,
                "region": default_region,
                "manifest_section_names": task.get("manifest_section_names"),
                "manifest_item_names": task.get("manifest_item_names"),
                "manifest_account_ids": task.get("manifest_account_ids"),
                "execution": task.get("execution"),
                "param_name": f"/sleeper/SleeperFunctionArn/{region}/stacks",
                "section_name": constants.SSM_PARAMETERS,
                "task_reference": expected_ssm_parameter_task_ref,
                "dependencies_by_reference": [],
                "dependencies": task.get("dependencies"),
            },
            all_tasks[expected_ssm_parameter_task_ref],
            "assert the boto3 task is generated correctly",
        )

        self.assertEqual(2, n_all_tasks, "assert the correct number of tasks exist")

    def test_for_ssm_parameters_for_hub_execution_mode(self):
        # setup
        puppet_account_id = "hub_account_id"
        account_id = "spoke_account_id"
        region = "eu-west-0"
        default_region = "eu-south-0"
        item_name = "depsrefactor"
        dependency_item_name = "something_else"

        task = {
            "stack_name": item_name,
            "launch_name": "",
            "stack_set_name": "",
            "capabilities": ["CAPABILITY_NAMED_IAM"],
            "ssm_param_outputs": [],
            "bucket": f"sc-puppet-stacks-repository-{puppet_account_id}",
            "key": f"stack/{item_name}/v1/stack.template-${{AWS::Region}}.yaml",
            "version_id": "",
            "execution": "hub",
            "use_service_role": True,
            "tags": [],
            "puppet_account_id": puppet_account_id,
            "status": None,
            "requested_priority": 0,
            "dependencies": [
                {"affinity": "stack", "name": dependency_item_name, "type": "stack",}
            ],
            "account_id": account_id,
            "region": region,
            "manifest_section_names": {"stacks": True},
            "manifest_item_names": {item_name: True},
            "manifest_account_ids": {account_id: True},
            "section_name": "stacks",
            "item_name": item_name,
            "dependencies_by_reference": [
                "create-policies",
                f"prepare-account-for-stacks-{account_id}",
                f"get-template-from-s3-stacks-{item_name}",
            ],
            "task_reference": f"{account_id}-{region}",
            "get_s3_template_ref": f"get-template-from-s3-stacks-{item_name}",
        }
        task_reference = task["task_reference"]
        all_tasks = {task_reference: task}

        parameter_path = "/sleeper/SleeperFunctionArn/${AWS::Region}/stacks"

        parameter_details = {
            "ssm": {"name": parameter_path, "account_id": "${AWS::AccountId}"}
        }

        # exercise
        self.sut.ssm_parameter_handler(
            all_tasks,
            default_region,
            all_tasks,
            parameter_details,
            puppet_account_id,
            task,
        )

        # verify
        n_all_tasks = len(all_tasks.keys())
        self.assertEqual(
            [
                "create-policies",
                f"prepare-account-for-stacks-{account_id}",
                f"get-template-from-s3-stacks-{item_name}",
                f"{constants.SSM_PARAMETERS}-{account_id}-{default_region}-{f'/sleeper/SleeperFunctionArn/{region}/stacks'}",
            ],
            all_tasks[task_reference].get("dependencies_by_reference"),
            "assert new dependency is added to the task needing the parameter",
        )

        expected_ssm_parameter_task_ref = f"{constants.SSM_PARAMETERS}-{account_id}-{default_region}-{f'/sleeper/SleeperFunctionArn/{region}/stacks'}"
        self.assertEqual(
            {
                "account_id": account_id,
                "region": default_region,
                "manifest_section_names": task.get("manifest_section_names"),
                "manifest_item_names": task.get("manifest_item_names"),
                "manifest_account_ids": task.get("manifest_account_ids"),
                "execution": task.get("execution"),
                "param_name": f"/sleeper/SleeperFunctionArn/{region}/stacks",
                "section_name": constants.SSM_PARAMETERS,
                "task_reference": expected_ssm_parameter_task_ref,
                "dependencies_by_reference": [],
                "dependencies": task.get("dependencies"),
            },
            all_tasks[expected_ssm_parameter_task_ref],
            "assert the boto3 task is generated correctly",
        )

        self.assertEqual(2, n_all_tasks, "assert the correct number of tasks exist")
