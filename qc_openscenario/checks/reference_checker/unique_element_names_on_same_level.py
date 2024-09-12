import logging

from dataclasses import dataclass
from typing import Union

from lxml import etree

from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.reference_checker import reference_checker_precondition
from collections import deque, defaultdict

CHECKER_ID = "check_asam_xosc_reference_control_unique_element_names_on_same_level"
MIN_RULE_VERSION = "1.2.0"


@dataclass
class QueueNode:
    element: etree._ElementTree
    parent_xpath: Union[str, None]


@dataclass
class DuplicateOccurrence:
    name: str
    xpath: str


def are_names_unique_at_each_level(tree: etree._ElementTree, root: etree._Element):
    # Initialize a queue for breadth-first traversal
    queue = deque([QueueNode(root, None)])
    levels_dict = defaultdict(set)

    duplicates = []

    while queue:
        queue_node = queue.popleft()

        current_element = queue_node.element
        current_name = current_element.get("name")
        parent_xpath = queue_node.parent_xpath
        current_xpath = tree.getpath(current_element)
        # Check if the element has a 'name' attribute
        if current_name is not None:
            # Check for duplicate names at the current level
            if current_name in levels_dict[parent_xpath]:
                logging.debug(f"Duplicated name found : {current_name}")
                duplicates.append(DuplicateOccurrence(current_name, current_xpath))
            levels_dict[parent_xpath].add(current_name)

        # Add children to the stack with incremented level
        for child in current_element.getchildren():
            queue.append(QueueNode(child, current_xpath))

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

    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        description="Element names at each level shall be unique at that level.",
    )

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting=MIN_RULE_VERSION,
        rule_full_name="reference_control.unique_element_names_on_same_level",
    )

    if not checker_data.result.all_checkers_completed_without_issue(
        reference_checker_precondition.PRECONDITIONS
    ):
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        return

    schema_version = checker_data.schema_version
    if (
        schema_version is None
        or utils.compare_versions(schema_version, MIN_RULE_VERSION) < 0
    ):
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        return

    tree = checker_data.input_file_xml_root
    duplicates_found = are_names_unique_at_each_level(tree, tree.getroot())

    for duplicate in duplicates_found:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when a element name is not unique within its level",
            level=IssueSeverity.ERROR,
            rule_uid=rule_uid,
        )
        issue_description = f"Element {duplicate.name} is duplicated"
        checker_data.result.add_xml_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            xpath=duplicate.xpath,
            description=issue_description,
        )

    checker_data.result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        status=StatusType.COMPLETED,
    )
