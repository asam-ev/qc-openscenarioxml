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
STORYBOARD_ELEMENTS = ["Act", "Action", "Event", "Maneuver", "ManeuverGroup", " Story"]


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xosc:1.2.0:reference_control.resolvable_storyboard_element_reference

    Description: The attribute storyboardElementRef shall point to an existing element
                 of the corresponding type and shall be uniquely resolvable.
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/29
    """
    logging.info("Executing resolvable_storyboard_element_reference check")

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
        rule_full_name="reference_control.resolvable_storyboard_element_reference",
    )

    root = checker_data.input_file_xml_root

    storyboard_node = root.find("Storyboard")
    if storyboard_node is None:
        logging.error(
            "Cannot find Storyboard node in provided XOSC file. Skipping check"
        )
        return

    xpath_expr = "|".join([f"//{node}" for node in STORYBOARD_ELEMENTS])
    storyboard_elements = storyboard_node.xpath(xpath_expr)
    if storyboard_elements is None:
        logging.error(
            "Cannot find Storyboard elements node in provided XOSC file. Skipping check"
        )
        return

    storyboard_element_names = set()
    for storyboard_element in list(storyboard_elements):
        current_name = storyboard_element.get("name")
        if current_name is not None:
            storyboard_element_names.add(current_name)

    logging.debug(f"storyboard_element_names: {storyboard_element_names}")

    nodes_with_storyboard_el_ref = storyboard_node.xpath(".//*[@storyboardElementRef]")

    for node_with_storyboard_el_ref in nodes_with_storyboard_el_ref:
        current_storyboard_el_ref = node_with_storyboard_el_ref.get(
            "storyboardElementRef"
        )
        logging.debug(f"current_storyboard_el_ref: {current_storyboard_el_ref}")

        # Check if entityRef points to a declared param
        if (
            utils.get_attribute_type(current_storyboard_el_ref)
            == models.AttributeType.PARAMETER
        ):
            current_entity_param_name = current_storyboard_el_ref[1:]
            current_entity_param_value = utils.get_parameter_value_from_node(
                root, node_with_storyboard_el_ref, current_entity_param_name
            )
            logging.debug(f"current_st_el_param_name: {current_entity_param_name}")
            logging.debug(f"current_st_el_param_value: {current_entity_param_value}")
            # Parameter value is assigned to the current_storyboard_el_ref to search
            # If parameter is not found, None is assigned to current_storyboard_el_ref
            current_storyboard_el_ref = current_entity_param_value

        has_issue = (
            current_storyboard_el_ref is None
            or current_storyboard_el_ref not in storyboard_element_names
        )

        if has_issue:
            xpath = root.getpath(node_with_storyboard_el_ref)

            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=reference_constants.CHECKER_ID,
                description="Issue flagging when a storyboardElementRef does not point to an existing element",
                level=RULE_SEVERITY,
                rule_uid=rule_uid,
            )
            issue_description = f"Storyboard element reference {current_storyboard_el_ref} not found among Storyboard elements "
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=reference_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=issue_description,
            )
