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


def are_names_unique_at_each_level(tree, root):
    # Initialize a queue for breadth-first traversal
    queue = deque([(root, None)])
    levels_dict = defaultdict(set)

    duplicates = []

    while queue:
        element, parent = queue.popleft()

        name = element.get("name")

        # Check if the element has a 'name' attribute
        if name is not None:
            # Check for duplicate names at the current level
            if name in levels_dict[parent]:
                logging.debug(f"Duplicated name found : {name}")
                duplicates.append((name, tree.getpath(element)))
            levels_dict[parent].add(name)

        # Add children to the stack with incremented level
        for child in element.getchildren():
            queue.append((child, element))

    return duplicates


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xosc:1.2.0:reference_control.unique_element_names_on_same_level

    Description: Element names at each level shall be unique at that level.
                 There shall not be more than one element with the same name at the same level
                 (within the same directly enclosing element).
                 For example, within one Story, every Act shall use a unique name ("MyStory1": "MyAct1", "MyAct2"…​),
                 but the names of the acts may be reused in another story ("MyStory2": "MyAct1", "MyAct2"…​).
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/30
    """
    logging.info("Executing unique_element_names_on_same_level check")

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
        rule_full_name="reference_control.unique_element_names_on_same_level",
    )

    tree = checker_data.input_file_xml_root
    duplicates_found = are_names_unique_at_each_level(tree, tree.getroot())

    for duplicate in duplicates_found:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=reference_constants.CHECKER_ID,
            description="Issue flagging when a element name is not unique within its level",
            level=RULE_SEVERITY,
            rule_uid=rule_uid,
        )
        issue_description = f"Element {duplicate[0]} is duplicated"
        checker_data.result.add_xml_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=reference_constants.CHECKER_ID,
            issue_id=issue_id,
            xpath=duplicate[1],
            description=issue_description,
        )
