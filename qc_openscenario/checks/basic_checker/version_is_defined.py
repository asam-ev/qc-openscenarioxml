import logging
from lxml import etree
from qc_baselib import IssueSeverity, Result, StatusType

from qc_openscenario import constants

from qc_openscenario.checks.basic_checker import (
    valid_xml_document,
    root_tag_is_openscenario,
    fileheader_is_present,
)

CHECKER_ID = "check_asam_xosc_xml_version_is_defined"
PRECONDITIONS = {
    valid_xml_document.CHECKER_ID,
    root_tag_is_openscenario.CHECKER_ID,
    fileheader_is_present.CHECKER_ID,
}


def is_unsigned_short(value: int) -> bool:
    """Helper function to check if a value is within the xsd:unsignedShort range (0-65535)."""
    try:
        num = int(value)
        return 0 <= num <= 65535
    except ValueError:
        return False


def check_rule(tree: etree._ElementTree, result: Result) -> None:
    """
    The FileHeader tag must have the attributes revMajor and revMinor and of type unsignedShort.

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/42
    """
    logging.info("Executing version_is_defined check")

    result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        description="The FileHeader tag must have the attributes revMajor and revMinor and of type unsignedShort.",
    )

    rule_uid = result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting="1.0.0",
        rule_full_name="xml.version_is_defined",
    )

    if not result.all_checkers_completed_without_issue(PRECONDITIONS):
        result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        return

    root = tree.getroot()

    is_valid = True
    # Check if root contains a tag 'FileHeader'
    file_header_tag = root.find("FileHeader")

    if file_header_tag is None:
        logging.error("- No FileHeader found, cannot check version. Skipping...")
        return True

    # Check if 'FileHeader' has the attributes 'revMajor' and 'revMinor'
    if (
        "revMajor" not in file_header_tag.attrib
        or "revMinor" not in file_header_tag.attrib
    ):
        logging.error("- 'FileHeader' tag does not have both 'revMajor' and 'revMinor'")
        is_valid = False

    if is_valid:
        # Check if 'attr1' and 'attr2' are xsd:unsignedShort (i.e., in the range 0-65535)
        rev_major = file_header_tag.attrib["revMajor"]
        rev_minor = file_header_tag.attrib["revMinor"]

        if not is_unsigned_short(rev_major) or not is_unsigned_short(rev_minor):
            logging.error(
                "- 'revMajor' and/or 'revMinor' are not xsd:unsignedShort (0-65535)"
            )
            is_valid = False

    if not is_valid:

        issue_id = result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when revMajor revMinor attribute of FileHeader are missing or invalid",
            level=IssueSeverity.ERROR,
            rule_uid=rule_uid,
        )

        result.add_xml_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            xpath=tree.getpath(file_header_tag),
            description=f'"FileHeader" tag has invalid or missing version info',
        )

    result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        status=StatusType.COMPLETED,
    )
