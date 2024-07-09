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
    Rule ID: asam.net:xosc:1.2.0:reference_control.valid_actor_reference_in_private_actions

    Description: In a ManeuverGroup, if the defined action is a private action an actor must be defined.

    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/17
    """
    logging.info("Executing valid_actor_reference_in_private_actions check")

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
        rule_full_name="reference_control.valid_actor_reference_in_private_actions",
    )

    root = checker_data.input_file_xml_root

    maneuver_groups = root.findall(".//ManeuverGroup")
    if maneuver_groups is None:
        logging.error(
            "Cannot find ManeuverGroup node in provided XOSC file. Skipping check"
        )
        return

    for maneuver_group in maneuver_groups:

        private_actions = maneuver_group.findall(".//PrivateAction")
        has_private_action = len(private_actions) > 0
        no_actor_provided = len(maneuver_group.find(".//Actors").getchildren()) == 0

        print(maneuver_group)
        print(maneuver_group.find(".//Actors"))
        print(list(maneuver_group.find(".//Actors")))

        has_issue = has_private_action and no_actor_provided

        if has_issue:
            xpath = get_xpath(
                root,
                maneuver_group,
            )
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=reference_constants.CHECKER_ID,
                description="Issue flagging when no Actor is specified but a PrivateAction is used",
                level=rule_severity,
                rule_uid=rule_uid,
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=reference_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"ManeuverGroup at {xpath} uses private actions {private_actions} but it defines no actor",
            )
