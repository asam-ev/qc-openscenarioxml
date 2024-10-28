# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from dataclasses import dataclass
from typing import Union, Optional

from lxml import etree

from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

import re
import enum

CHECKER_ID = "check_asam_xosc_data_type_allowed_operators"
CHECKER_DESCRIPTION = "Expressions in OpenSCENARIO must only use the allowed operands."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.2.0:data_type.allowed_operators"

ALLOWED_OPERANDS = set()
ALLOWED_OPERANDS.add("-")
ALLOWED_OPERANDS.add("round")
ALLOWED_OPERANDS.add("floor")
ALLOWED_OPERANDS.add("ceil")
ALLOWED_OPERANDS.add("sqrt")
ALLOWED_OPERANDS.add("pow")
ALLOWED_OPERANDS.add("*")
ALLOWED_OPERANDS.add("/")
ALLOWED_OPERANDS.add("%")
ALLOWED_OPERANDS.add("+")
ALLOWED_OPERANDS.add("not")
ALLOWED_OPERANDS.add("and")
ALLOWED_OPERANDS.add("or")


class ExpressionMember(enum.IntEnum):
    INVALID = 0
    VARIABLE = 1
    OPERATOR = 2
    NUMBER = 3
    PARENTHESIS = 4


@dataclass
class QueueNode:
    element: etree._ElementTree
    xpath: Optional[str]


@dataclass
class AttributeInfo:
    name: str
    value: str
    xpath: str


def get_all_attributes(tree: etree._ElementTree, root: etree._Element):
    attributes = []
    stack = [
        QueueNode(root, tree.getpath(root))
    ]  # Initialize stack with the root element

    while stack:
        current_node = stack.pop()
        current_element = current_node.element
        current_xpath = current_node.xpath

        # Process attributes of the current element
        for attr, value in current_element.attrib.items():
            attributes.append(AttributeInfo(attr, value, current_xpath))

        # Push children to the stack for further processing
        stack.extend(
            reversed(
                [QueueNode(x, tree.getpath(x)) for x in current_element.getchildren()]
            )
        )

    return attributes


def filter_expressions(attribute):
    return (
        attribute.value.startswith("$")
        and utils.get_attribute_type(attribute.value) != models.AttributeType.PARAMETER
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

    tree = checker_data.input_file_xml_root
    root = tree.getroot()
    attributes = get_all_attributes(tree, root)
    filtered_attributes = list(filter(filter_expressions, attributes))

    logging.debug(f"attributes: {attributes}")
    logging.debug(f"filtered_attributes: {filtered_attributes}")

    for attribute in filtered_attributes:
        # Remove starting "${" and trailing "}"
        expression_candidate = attribute.value[2:-1]
        logging.debug(f"expression_candidate: {expression_candidate}")

        # Tokenize the expression using regular expressions
        token_pattern = r"\$[A-Za-z_]\w*|\d+\.\d+|\d+|[\+\-\*/\^%()**//\{\}]|\w+"
        tokens = re.findall(token_pattern, expression_candidate)

        token_type = None
        logging.debug(f"tokens: {tokens}")
        for token in tokens:
            if token.startswith("$"):
                token_type = ExpressionMember.VARIABLE
            elif token in ALLOWED_OPERANDS:
                token_type = ExpressionMember.OPERATOR
            elif re.match(r"\d+\.\d+", token) or token.isdigit():
                token_type = ExpressionMember.NUMBER
            elif token in ["(", ")"]:
                token_type = ExpressionMember.PARENTHESIS
            else:
                token_type = ExpressionMember.INVALID

            logging.debug(f"token {token} - type {token_type}")
            if token_type is None:
                continue

            has_issue = token_type == ExpressionMember.INVALID
            if has_issue:
                logging.debug(f"Invalid operand {token}")
                xpath = attribute.xpath

                issue_id = checker_data.result.register_issue(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=CHECKER_ID,
                    description="Invalid operand used within expression",
                    level=IssueSeverity.ERROR,
                    rule_uid=RULE_UID,
                )
                checker_data.result.add_xml_location(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=CHECKER_ID,
                    issue_id=issue_id,
                    xpath=xpath,
                    description=f"Invalid operand {token} used",
                )
