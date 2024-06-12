import logging

from dataclasses import dataclass
from typing import List

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.xml_checker import xml_constants


def is_valid_xml(file_path):
    try:
        with open(file_path, "rb") as file:
            xml_content = file.read()
            etree.fromstring(xml_content)
            print("The XML is valid.")
        return True, None
    except etree.XMLSyntaxError as e:
        print(f"Error: {e}")
        print(f"Error occurred at line {e.lineno}, column {e.offset}")
        return False, (e.lineno, e.offset)


def check_rule(input_xml_file_path, result) -> bool:
    """
    Implements a rule to check if input file is a valid xml document
    """
    logging.info("Executing is_an_xml_document check")

    rule_uid = result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=xml_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting="1.0.0",
        rule_full_name="xml.is_an_xml_document",
    )

    is_valid, error_location = is_valid_xml(input_xml_file_path)

    if not is_valid:

        issue_id = result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=xml_constants.CHECKER_ID,
            description="Issue flagging when input file is not a valid xml document",
            level=IssueSeverity.ERROR,
            rule_uid=rule_uid,
        )

        result.add_file_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=xml_constants.CHECKER_ID,
            issue_id=issue_id,
            row=error_location[0],
            column=error_location[1],
            file_type="xosc",
            description=f"Invalid xml detected",
        )

        return False

    return True
