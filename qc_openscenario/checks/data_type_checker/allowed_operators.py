import os, logging

from dataclasses import dataclass
from typing import List

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.schema import schema_files
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.data_type_checker import data_type_constants

import re

MIN_RULE_VERSION = "1.2.0"
RULE_SEVERITY = IssueSeverity.ERROR
ALLOWED_OPERANDS = [
    "-",
    "round",
    "floor",
    "ceil",
    "sqrt",
    "pow",
    "*",
    "/",
    "%",
    "+",
    "-",
    "not",
    "and",
    "or",
]


def get_all_attributes(tree, root):
    attributes = []
    stack = [root]  # Initialize stack with the root element

    while stack:
        current = stack.pop()

        # Process attributes of the current element
        for attr, value in current.attrib.items():
            attributes.append((attr, value, tree.getpath(current)))

        # Push children to the stack for further processing
        stack.extend(reversed(current.getchildren()))

    return attributes


def filter_expressions(attribute):
    _, attr_value, _ = attribute
    return (
        attr_value.startswith("$")
        and utils.get_attribute_type(attr_value) != models.AttributeType.PARAMETER
    )


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xosc:1.2.0:data_type.allowed_operators

    Description: Expressions in OpenSCENARIO must only use the following operands:
                 -, round, floor, ceil, sqrt, pow, *, /, %, +, -, not, and, or.
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/31
    """
    logging.info("Executing allowed_operators check")

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
        rule_full_name="data_type.allowed_operators",
    )

    tree = checker_data.input_file_xml_root
    root = tree.getroot()
    attributes = get_all_attributes(tree, root)
    filtered_attributes = list(filter(filter_expressions, attributes))

    logging.debug(f"attributes: {attributes}")
    logging.debug(f"filtered_attributes: {filtered_attributes}")

    for attribute in filtered_attributes:
        expression_candidate = attribute[1][2:-1]
        logging.debug(f"expression_candidate: {expression_candidate}")
        # Define the regex pattern to match digits and allowed chars ( ) . and ,
        pattern = r"[\d()., ]+"
        # Split the input string based on the regex pattern
        operands_candidates = re.split(pattern, expression_candidate)
        # Filter out empty strings from the resulting list
        operands_candidates = [
            part for part in operands_candidates if part and part != "" and part != " "
        ]

        for operand in operands_candidates:
            has_issue = operand not in ALLOWED_OPERANDS
            if has_issue:
                logging.debug(f"Invalid operand {operand}")
                xpath = attribute[2]

                issue_id = checker_data.result.register_issue(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=data_type_constants.CHECKER_ID,
                    description="Issue flagging invalid operand is used within expession",
                    level=RULE_SEVERITY,
                    rule_uid=rule_uid,
                )
                checker_data.result.add_xml_location(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=data_type_constants.CHECKER_ID,
                    issue_id=issue_id,
                    xpath=xpath,
                    description=f"Invalid operand {operand} used",
                )
