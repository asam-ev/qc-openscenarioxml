import logging
from qc_baselib import IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import models

from qc_openscenario.checks.basic_checker import valid_xml_document

CHECKER_ID = "check_asam_xosc_xml_root_tag_is_openscenario"
CHECKER_DESCRIPTION = "The root element of a valid XML document must be OpenSCENARIO."
CHECKER_PRECONDITIONS = {valid_xml_document.CHECKER_ID}
RULE_UID = "asam.net:xosc:1.0.0:xml.root_tag_is_openscenario"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    The root element of a valid XML document must be OpenSCENARIO

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/40
    """
    logging.info("Executing root_tag_is_openscenario check")

    root = checker_data.input_file_xml_root.getroot()

    is_valid = False
    if root.tag == "OpenSCENARIO":
        logging.info("- Root tag is 'OpenSCENARIO'")
        is_valid = True
    else:
        logging.error("- Root tag is not 'OpenSCENARIO'")
        is_valid = False

    if not is_valid:

        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when root tag is not OpenSCENARIO",
            level=IssueSeverity.ERROR,
            rule_uid=RULE_UID,
        )

        checker_data.result.add_xml_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            xpath=checker_data.input_file_xml_root.getpath(root),
            description=f"Root is not OpenSCENARIO",
        )
