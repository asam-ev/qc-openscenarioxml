import os, logging

from dataclasses import dataclass
from typing import List

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.schema import schema_files
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.reference_checker import reference_constants
from collections import deque, defaultdict

MIN_RULE_VERSION = "1.2.0"
RULE_SEVERITY = IssueSeverity.ERROR


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

    schema_version = checker_data.schema_version
    if schema_version is None:
        logging.info(f"- Version not found in the file. Skipping check")
        return

    if utils.compare_versions(schema_version, MIN_RULE_VERSION) < 0:
        logging.info(
            f"- Version {schema_version} is less than minimum required version {MIN_RULE_VERSION}. Skipping check"
        )
        return

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting=MIN_RULE_VERSION,
        rule_full_name="reference_control.resolvable_entity_references",
    )

    root = checker_data.input_file_xml_root

    entities_node = root.find("Entities")
    if entities_node is None:
        logging.error("Cannot find Entities node in provided XOSC file. Skipping check")
        return

    defined_entities = set()
    for entity_node in list(entities_node):
        current_name = entity_node.get("name")
        if current_name is not None:
            defined_entities.add(current_name)

    logging.debug(f"Defined entities : {defined_entities}")
    storyboard_node = root.find("Storyboard")
    if storyboard_node is None:
        logging.error(
            "Cannot find Storyboard node in provided XOSC file. Skipping check"
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
            current_entity_param_value = utils.get_parameter_value(
                root, current_entity_param_name
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
                checker_id=reference_constants.CHECKER_ID,
                description="Issue flagging when an entity is referred in a entityRef attribute but it is not declared among Entities",
                level=RULE_SEVERITY,
                rule_uid=rule_uid,
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=reference_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"Entity at {xpath} with id {current_entity_ref} not found among defined Entities ",
            )
