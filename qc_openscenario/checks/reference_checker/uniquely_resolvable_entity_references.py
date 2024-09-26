import logging

from typing import List

from lxml import etree

from qc_baselib import IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import models
from qc_openscenario import basic_preconditions


CHECKER_ID = "check_asam_xosc_reference_control_uniquely_resolvable_entity_references"
CHECKER_DESCRIPTION = "Reference names must be unique"
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.2.0:reference_control.uniquely_resolvable_entity_references"


def get_catalogs(root: etree._ElementTree) -> List[etree._ElementTree]:
    catalogs = []

    for catalog in root.iter("Catalog"):
        catalogs.append(catalog)

    return catalogs


def get_xpath(root: etree._ElementTree, element: etree._ElementTree) -> str:
    return root.getpath(element)


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if referenced entities are unique

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/8
    """
    logging.info("Executing uniquely_resolvable_entity_references check")

    root = checker_data.input_file_xml_root

    # List to store problematic nodes
    errors = []

    # Iterate over each 'Catalog' node
    for catalog_node in root.findall(".//Catalog"):
        # Dictionary to track child nodes by 'name' attribute
        child_names = {}

        # Iterate catalog children within current 'Catalog' node
        # Currently the checks verifies that the same name is not used in the same
        # catalog regardless the tag type
        # E.g. Catalog children:
        # # [Vehicle name="abc", Maneuver name="abc"]
        # Will trigger the issue
        for child_node in catalog_node.iterchildren():
            name_attr = child_node.attrib.get("name")
            if name_attr:
                if name_attr in child_names:
                    errors.append(
                        {
                            "name": name_attr,
                            "tag": child_node.tag,
                            "first_xpath": get_xpath(root, child_names[name_attr]),
                            "duplicate_xpath": get_xpath(root, child_node),
                        }
                    )
                else:
                    child_names[name_attr] = child_node

    if len(errors) > 0:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Referenced entity name duplicated",
            level=IssueSeverity.WARNING,
            rule_uid=RULE_UID,
        )

        for error in errors:
            error_name = error["name"]
            error_first_xpath = error["first_xpath"]
            error_duplicate_xpath = error["duplicate_xpath"]
            error_msg = f"Duplicate name {error_name}. First occurrence at {error_first_xpath} duplicate at {error_duplicate_xpath}"
            logging.error(f"- Error: {error_msg}")
            logging.error(f"- Duplicate xpath: {error_duplicate_xpath}")
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=error_duplicate_xpath,
                description=error_msg,
            )
