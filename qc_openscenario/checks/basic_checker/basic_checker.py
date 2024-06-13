import logging

from lxml import etree

from qc_baselib import Configuration, Result, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.basic_checker import (
    basic_constants,
    is_an_xml_document,
)


def run_checks(config: Configuration, result: Result) -> models.CheckerData:
    logging.info("Executing basic checks")

    result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=basic_constants.CHECKER_ID,
        description="Check if basic properties of input file are properly set",
        summary="",
    )

    xml_file_path = config.get_config_param("XoscFile")
    is_xml = is_an_xml_document.check_rule(xml_file_path, result)

    checker_data = None

    if not is_xml:
        logging.error("Error in input xml!")
        checker_data = models.CheckerData(
            input_file_xml_root=None,
            config=config,
            result=result,
            schema_version="0.0",
        )

    else:
        root = etree.parse(config.get_config_param("XoscFile"))
        xosc_schema_version = utils.get_standard_schema_version(root)

        checker_data = models.CheckerData(
            input_file_xml_root=root,
            config=config,
            result=result,
            schema_version=xosc_schema_version,
        )

    logging.info(
        f"Issues found - {result.get_checker_issue_count(checker_bundle_name=constants.BUNDLE_NAME, checker_id=basic_constants.CHECKER_ID)}"
    )

    # TODO: Add logic to deal with error or to skip it
    result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=basic_constants.CHECKER_ID,
        status=StatusType.COMPLETED,
    )

    return checker_data
