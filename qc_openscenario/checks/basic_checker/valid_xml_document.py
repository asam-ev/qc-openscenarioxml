import logging

from lxml import etree

from qc_baselib import Result, IssueSeverity, StatusType
from qc_openscenario import constants

CHECKER_ID = "check_asam_xosc_xml_valid_xml_document"


def _is_xml_doc(file_path: str) -> tuple[bool, tuple[int, int]]:
    try:
        with open(file_path, "rb") as file:
            xml_content = file.read()
            etree.fromstring(xml_content)
            logging.info("- It is an xml document.")
        return True, None
    except etree.XMLSyntaxError as e:
        logging.error(f"- Error: {e}")
        logging.error(f"- Error occurred at line {e.lineno}, column {e.offset}")
        return False, (e.lineno, e.offset)


def check_rule(input_xml_file_path: str, result: Result) -> None:
    """
    Implements a rule to check if input file is a valid xml document

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/1
    """
    logging.info("Executing valid_xml_document check")

    result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        description="The given file to check must be a valid XML document.",
    )

    rule_uid = result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting="1.0.0",
        rule_full_name="xml.valid_xml_document",
    )

    is_valid, error_location = _is_xml_doc(input_xml_file_path)

    if not is_valid:

        issue_id = result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="The input file is not a valid xml document",
            level=IssueSeverity.ERROR,
            rule_uid=rule_uid,
        )

        result.add_file_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            row=error_location[0],
            column=error_location[1],
            description=f"Invalid xml file.",
        )

    result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        status=StatusType.COMPLETED,
    )
