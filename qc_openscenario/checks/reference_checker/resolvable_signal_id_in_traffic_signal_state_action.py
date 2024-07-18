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
    Rule ID: asam.net:xosc:1.2.0:reference_control.resolvable_signal_id_in_traffic_signal_state_action

    Description: TrafficSignalStateAction:name -> Signal ID must exist within the given road network
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/13
    """
    logging.info("Executing resolvable_signal_id_in_traffic_signal_state_action check")

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
        rule_full_name="reference_control.resolvable_signal_id_in_traffic_signal_state_action",
    )

    root = checker_data.input_file_xml_root

    if checker_data.xodr_root is None:
        logging.error(f" - Cannot read xodr file. Abort")
        return

    xodr_signal_list = checker_data.xodr_root.findall(".//signal")

    if xodr_signal_list is None:
        logging.error(f" - Cannot read signals from xodr file. Abort")
        return

    xodr_signal_ids = set()
    for xodr_signal in xodr_signal_list:
        signal_id = xodr_signal.get("id")
        if signal_id is not None:
            xodr_signal_ids.add(signal_id)

    xosc_traffic_lights = root.findall(".//TrafficSignalStateAction")

    for xosc_traffic_light in xosc_traffic_lights:
        current_name = xosc_traffic_light.get("name")

        if current_name is not None and current_name not in xodr_signal_ids:
            xpath = root.getpath(xosc_traffic_light)
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=reference_constants.CHECKER_ID,
                description="Issue flagging traffic light id not present in linked xodr file",
                level=RULE_SEVERITY,
                rule_uid=rule_uid,
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=reference_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"Traffic Light {xpath} with id {current_name} not found in xodr file",
            )
