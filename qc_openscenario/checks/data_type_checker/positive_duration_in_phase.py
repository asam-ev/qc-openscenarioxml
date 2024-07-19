import os, logging

from dataclasses import dataclass
from typing import List

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.schema import schema_files
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.data_type_checker import data_type_constants

MIN_RULE_VERSION = "1.2.0"
RULE_SEVERITY = IssueSeverity.ERROR


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xosc:1.2.0:data_type.positive_duration_in_phase

    Description: Attribute “duration” in the complex type “Phase” (e.g., for TrafficSignalController”) shall be non-negative.
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/33
    """
    logging.info("Executing positive_duration_in_phase check")

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
        checker_id=data_type_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting=MIN_RULE_VERSION,
        rule_full_name="data_type.positive_duration_in_phase",
    )

    root = checker_data.input_file_xml_root

    phase_nodes = root.findall(".//Phase")

    for phase_node in phase_nodes:
        current_duration = phase_node.get("duration")
        logging.debug(f"current_duration: {current_duration}")
        current_duration_type = utils.get_attribute_type(current_duration)

        if current_duration is None:
            continue
        if current_duration_type == models.AttributeType.EXPRESSION:
            logging.debug(
                f"Skipping duration with value {current_duration} since sign cannot be evaluated "
            )
            continue
        if current_duration_type == models.AttributeType.PARAMETER:
            current_duration_param_name = current_duration[1:]
            current_duration_param_value = utils.get_parameter_value_from_node(
                root, phase_node, current_duration_param_name
            )
            logging.debug(f"current_duration_param_name: {current_duration_param_name}")
            logging.debug(
                f"current_duration_param_value: {current_duration_param_value}"
            )
            # Parameter value is assigned to the current_transition_time to search
            # If parameter is not found, None is assigned to current_storyboard_el_ref
            if current_duration_param_value is None:
                continue
            current_duration = current_duration_param_value

        current_numeric_value = float(current_duration)
        has_issue = current_numeric_value < 0

        if has_issue:
            xpath = root.getpath(phase_node)

            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=data_type_constants.CHECKER_ID,
                description="Issue flagging when attribute “duration” in the complex type “Phase” is negative",
                level=RULE_SEVERITY,
                rule_uid=rule_uid,
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=data_type_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"Phase duration {current_numeric_value} is negative",
            )
