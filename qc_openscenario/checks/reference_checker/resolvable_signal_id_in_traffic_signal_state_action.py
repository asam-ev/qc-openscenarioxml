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


def get_xpath(root: etree._ElementTree, element: etree._ElementTree) -> str:
    return root.getpath(element)


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

    rule_severity = IssueSeverity.ERROR
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

    input_file_path = checker_data.config.get_config_param("XoscFile")
    # Store previous working directory and move to config path dir for relative package paths
    previous_wd = os.getcwd()
    os.chdir(os.path.dirname(input_file_path))

    root = checker_data.input_file_xml_root

    xodr_path = utils.get_xodr_file(root)

    if xodr_path is None or not os.path.isfile(xodr_path):
        logging.error(f"Cannot read xodr path {xodr_path}. File not found. Abort")
        os.chdir(previous_wd)
        return

    xodr_root = etree.parse(xodr_path)

    xodr_signal_list = xodr_root.findall(".//signal")

    xodr_signal_ids = []
    for xodr_signal in xodr_signal_list:
        xodr_signal_ids.append(xodr_signal.get("id"))

    xosc_traffic_lights = root.findall(".//TrafficSignalStateAction")

    for xosc_traffic_light in xosc_traffic_lights:
        current_name = xosc_traffic_light.get("name")
        if current_name not in xodr_signal_ids:
            xpath = get_xpath(
                root,
                xosc_traffic_light,
            )
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=reference_constants.CHECKER_ID,
                description="Issue flagging traffic light id not present in linked xodr file",
                level=rule_severity,
                rule_uid=rule_uid,
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=reference_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"Traffic Light {xpath} with id {current_name} not found in xodr file {xodr_path}",
            )
    os.chdir(previous_wd)
