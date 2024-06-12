import logging

from dataclasses import dataclass
from typing import List

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.xml_checker import xml_constants


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if there is mixed content on access rules for
    the same sOffset on lanes.

    """
    logging.info("Executing is_an_xml_document check")
    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=xml_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting=checker_data.schema_version,
        rule_full_name="is_an_xml_document",
    )

    issue_id = checker_data.result.register_issue(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=xml_constants.CHECKER_ID,
        description="Test issue",
        level=IssueSeverity.ERROR,
        rule_uid=rule_uid,
    )

    checker_data.result.add_inertial_location(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=xml_constants.CHECKER_ID,
        issue_id=issue_id,
        x=1.0,
        y=2.0,
        z=3.0,
        description=f"First encounter of issue",
    )

    print("Rule uid: ", rule_uid)
