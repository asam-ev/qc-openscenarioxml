import logging
from lxml import etree
from qc_baselib import IssueSeverity, Result

from qc_openscenario import constants
from qc_openscenario.checks import models

from qc_openscenario.checks.basic_checker import basic_constants


def check_rule(tree: etree._ElementTree, result: Result) -> bool:
    """
    Below the root element a tag with FileHeader must be defined

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/41
    """
    logging.info("Executing fileheader_is_present check")

    rule_uid = result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=basic_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting="1.0.0",
        rule_full_name="xml.fileheader_is_present",
    )

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
            checker_id=basic_constants.CHECKER_ID,
            description="Issue flagging when no FileHeader is found under root element",
            level=IssueSeverity.ERROR,
            rule_uid=rule_uid,
        )

        result.add_xml_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=basic_constants.CHECKER_ID,
            issue_id=issue_id,
            xpath=tree.getpath(root),
            description=f'No child element "FileHeader"',
        )

        return False

    return True
