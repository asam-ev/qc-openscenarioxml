import logging

from lxml import etree

from qc_baselib import Configuration, Result, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.xml_checker import (
    xml_constants,
    is_an_xml_document,
)


def run_checks(config: Configuration, result: Result) -> None:
    logging.info("Executing xml checks")

    result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=xml_constants.CHECKER_ID,
        description="Check if xml properties of input file are properly set",
        summary="",
    )

    xml_file_path = config.get_config_param("XoscFile")
    valid_xml = is_an_xml_document.check_rule(xml_file_path, result)

    if not valid_xml:
        print("Error in input xml, skipping all other checks")
    else:
        root = etree.parse(config.get_config_param("XoscFile"))
        xosc_schema_version = utils.get_standard_schema_version(root)

        rule_list = []

        checker_data = models.CheckerData(
            input_file_xml_root=root,
            config=config,
            result=result,
            schema_version=xosc_schema_version,
        )

        for rule in rule_list:
            rule(xml_file_path, checker_data=checker_data)

    logging.info(
        f"Issues found - {result.get_checker_issue_count(checker_bundle_name=constants.BUNDLE_NAME, checker_id=xml_constants.CHECKER_ID)}"
    )

    # TODO: Add logic to deal with error or to skip it
    result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=xml_constants.CHECKER_ID,
        status=StatusType.COMPLETED,
    )
