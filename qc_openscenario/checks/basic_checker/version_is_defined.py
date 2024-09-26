import logging

from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import models

from qc_openscenario.checks.basic_checker import (
    valid_xml_document,
    root_tag_is_openscenario,
    fileheader_is_present,
)

CHECKER_ID = "check_asam_xosc_xml_version_is_defined"
CHECKER_DESCRIPTION = "The FileHeader tag must have the attributes revMajor and revMinor and of type unsignedShort."
CHECKER_PRECONDITIONS = {
    valid_xml_document.CHECKER_ID,
    root_tag_is_openscenario.CHECKER_ID,
    fileheader_is_present.CHECKER_ID,
}
RULE_UID = "asam.net:xosc:1.0.0:xml.version_is_defined"


def is_unsigned_short(value: int) -> bool:
    """Helper function to check if a value is within the xsd:unsignedShort range (0-65535)."""
    try:
        num = int(value)
        return 0 <= num <= 65535
    except ValueError:
        return False


def check_rule(checker_data: models.CheckerData) -> None:
    """
    The FileHeader tag must have the attributes revMajor and revMinor and of type unsignedShort.

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/42
    """
    logging.info("Executing version_is_defined check")

    root = checker_data.input_file_xml_root.getroot()

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

        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Version attributes revMajor-revMinor missing or invalid",
            level=IssueSeverity.ERROR,
            rule_uid=RULE_UID,
        )

        checker_data.result.add_xml_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            xpath=checker_data.input_file_xml_root.getpath(file_header_tag),
            description=f'"FileHeader" tag has invalid or missing version info',
        )
