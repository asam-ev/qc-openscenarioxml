import logging
from lxml import etree
from qc_baselib import IssueSeverity, Result

from qc_openscenario import constants
from qc_openscenario.checks import models

from qc_openscenario.checks.basic_checker import basic_constants


def check_rule(tree: etree._ElementTree, result: Result) -> bool:
    """
    The root element of a valid XML document must be OpenSCENARIO

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/40
    """
    logging.info("Executing root_tag_is_openscenario check")

    rule_uid = result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=basic_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting="1.0.0",
        rule_full_name="xml.root_tag_is_openscenario",
    )

    root = tree.getroot()

    is_valid = False
    if root.tag == "OpenSCENARIO":
        logging.info("- Root tag is 'OpenSCENARIO'")
        is_valid = True
    else:
        logging.error("- Root tag is not 'OpenSCENARIO'")
        is_valid = False

    if not is_valid:

        issue_id = result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=basic_constants.CHECKER_ID,
            description="Issue flagging when root tag is not OpenSCENARIO",
            level=IssueSeverity.ERROR,
            rule_uid=rule_uid,
        )

        result.add_xml_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=basic_constants.CHECKER_ID,
            issue_id=issue_id,
            xpath=tree.getpath(root),
            description=f"Root is not OpenSCENARIO",
        )

        return False

    return True
