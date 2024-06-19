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

    schema_version = checker_data.schema_version
    if schema_version is None:
        logging.info(f"- Version not found in the file. Skipping check")
        return

    min_rule_version = "1.2.0"
    rule_severity = IssueSeverity.WARNING
    if utils.compare_versions(schema_version, min_rule_version) < 0:
        logging.info(
            f"- Version {schema_version} is less than minimum required version {min_rule_version}. Skipping check"
        )
        return

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting="1.2.0",
        rule_full_name="reference_control.uniquely_resolvable_entity_references",
    )

    root = checker_data.input_file_xml_root

    # List to store problematic vehicle nodes
    errors = []

    # Iterate over each 'Catalog' node
    for catalog_node in root.findall(".//Catalog"):
        # Dictionary to track 'vehicle' nodes by 'name' attribute
        vehicle_names = {}

        # Iterate over 'Vehicle' nodes within current 'Catalog' node
        for vehicle_node in catalog_node.findall(".//Vehicle"):
            name_attr = vehicle_node.attrib.get("name")
            if name_attr:
                if name_attr in vehicle_names:
                    errors.append(
                        {
                            "name": name_attr,
                            "tag": vehicle_node.tag,
                            "first_xpath": get_xpath(root, vehicle_names[name_attr]),
                            "duplicate_xpath": get_xpath(root, vehicle_node),
                        }
                    )
                else:
                    vehicle_names[name_attr] = vehicle_node

    if len(errors) > 0:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=reference_constants.CHECKER_ID,
            description="Issue flagging when referenced names are not unique",
            level=rule_severity,
            rule_uid=rule_uid,
        )

        for error in errors:
            error_name = error["name"]
            error_first_xpath = error["first_xpath"]
            error_duplicate_xpath = error["duplicate_xpath"]
            error_msg = f"Duplicate vehicle name {error_name}. First occurrence at {error_first_xpath} duplicate at {error_duplicate_xpath}"
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=reference_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=error_duplicate_xpath,
                description=error_msg,
            )
