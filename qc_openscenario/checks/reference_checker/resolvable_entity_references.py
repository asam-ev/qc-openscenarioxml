# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models
from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_reference_control_resolvable_entity_references"
CHECKER_DESCRIPTION = "A named reference in the EntityRef must be resolvable."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.2.0:reference_control.resolvable_entity_references"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xosc:1.2.0:reference_control.resolvable_entity_references

    Description: A named reference in the EntityRef must be resolvable. Checking all EntityRef's in the document.
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/15
    """
    logging.info("Executing resolvable_entity_references check")

    root = checker_data.input_file_xml_root

    entities_node = root.find("Entities")
    if entities_node is None:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            "Cannot find Entities node in provided XOSC file. Skip the check.",
        )

        return

    defined_entities = set()
    for entity_node in list(entities_node):
        current_name = entity_node.get("name")
        if current_name is not None:
            defined_entities.add(current_name)

    logging.debug(f"Defined entities : {defined_entities}")
    storyboard_node = root.find("Storyboard")
    if storyboard_node is None:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            "Cannot find Storyboard node in provided XOSC file. Skip the check.",
        )

        return

    nodes_with_entity_ref = storyboard_node.xpath(".//*[@entityRef]")

    for node_with_entity_ref in nodes_with_entity_ref:
        current_entity_ref = node_with_entity_ref.get("entityRef")

        if current_entity_ref is None:
            continue

        has_issue = False

        # Check if entityRef points to a declared param
        if (
            utils.get_attribute_type(current_entity_ref)
            == models.AttributeType.PARAMETER
        ):
            current_entity_param_name = current_entity_ref[1:]
            current_entity_param_value = utils.get_parameter_value_from_node(
                root, node_with_entity_ref, current_entity_param_name
            )
            logging.debug(f"current_entity_param_name: {current_entity_param_name}")
            logging.debug(f"current_entity_param_value: {current_entity_param_value}")
            # Parameter value is assigned to the current_entity_ref to search
            # If parameter is not found, None is assigned to current_entity_ref
            current_entity_ref = current_entity_param_value

        has_issue = (
            current_entity_ref is None or current_entity_ref not in defined_entities
        )

        if has_issue:
            xpath = root.getpath(node_with_entity_ref)

            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="Entity not declared among Entities but referred in an entityRef attribute",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"Entity at {xpath} with id {current_entity_ref} not found among defined Entities ",
            )
