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
    Rule ID: asam.net:xosc:1.2.0:reference_control.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref

    Description: The trafficSignalController according to the "trafficSignalControllerRef" property must exist within the scenarios RoadNetwork definition.
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/14
    """
    logging.info(
        "Executing resolvable_traffic_signal_controller_by_traffic_signal_controller_ref check"
    )

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
        rule_full_name="reference_control.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref",
    )

    root = checker_data.input_file_xml_root

    road_network = root.find("RoadNetwork")
    if road_network is None:
        logging.error(
            "Cannot find RoadNetwork node in provided XOSC file. Skipping check"
        )
        return

    # ts = traffic signal
    ts_controllers = road_network.findall(".//TrafficSignalController")
    if ts_controllers is None:
        logging.error(
            "Cannot find TrafficSignalController nodes in RoadNetwork of provided XOSC file. Skipping check"
        )
        return

    ts_controller_names = [x.get("name") for x in ts_controllers]

    ts_controller_actions = root.findall(".//TrafficSignalControllerAction")

    for ts_controller in ts_controller_actions:
        current_name = ts_controller.get("trafficSignalControllerRef")
        if current_name not in ts_controller_names:
            xpath = get_xpath(
                root,
                ts_controller,
            )
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=reference_constants.CHECKER_ID,
                description="Issue flagging traffic signal controller reference not present in the declared RoadNetwork",
                level=rule_severity,
                rule_uid=rule_uid,
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=reference_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"trafficSignalControllerRef at {xpath} with id {current_name} not found in RoadNetwork node",
            )
