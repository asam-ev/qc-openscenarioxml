import logging
from lxml import etree
from qc_baselib import IssueSeverity, Result, StatusType

from qc_openscenario import constants

from qc_openscenario.checks.basic_checker import (
    valid_xml_document,
    root_tag_is_openscenario,
)

CHECKER_ID = "check_asam_xosc_xml_fileheader_is_present"
PRECONDITIONS = {valid_xml_document.CHECKER_ID, root_tag_is_openscenario.CHECKER_ID}


def check_rule(tree: etree._ElementTree, result: Result) -> None:
    """
    Below the root element a tag with FileHeader must be defined.

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/41
    """
    logging.info("Executing fileheader_is_present check")

    result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        description="Below the root element a tag with FileHeader must be defined.",
    )

    rule_uid = result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting="1.0.0",
        rule_full_name="xml.fileheader_is_present",
    )

    if not result.all_checkers_completed_without_issue(PRECONDITIONS):
        result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        return

    root = tree.getroot()

    is_valid = False
    # Check if root contains a tag 'FileHeader'
    file_header_tag = root.find("FileHeader")
    if file_header_tag is not None:
        logging.info("- Root tag contains FileHeader -> OK")
        is_valid = True
    else:
        logging.error("- FileHeader not found under root element")
        is_valid = False

    if not is_valid:

        issue_id = result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when no FileHeader is found under root element",
            level=IssueSeverity.ERROR,
            rule_uid=rule_uid,
        )

        result.add_xml_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            xpath=tree.getpath(root),
            description=f'No child element "FileHeader"',
        )

    result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        status=StatusType.COMPLETED,
    )
