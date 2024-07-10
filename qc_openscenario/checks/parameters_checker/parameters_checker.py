import logging

from lxml import etree

from qc_baselib import Configuration, Result, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models
from qc_openscenario.schema import schema_files

from qc_openscenario.checks.parameters_checker import (
    parameters_constants,
    valid_parameter_declaration_in_catalogs,
)


def run_checks(checker_data: models.CheckerData) -> None:
    logging.info("Executing parameters checks")

    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=parameters_constants.CHECKER_ID,
        description="Check if parameters properties of input file are properly set",
        summary="",
    )

    if checker_data.input_file_xml_root is None:
        logging.error(
            f"Invalid xml input file. Checker {parameters_constants.CHECKER_ID} skipped"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=parameters_constants.CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    if checker_data.schema_version not in schema_files.SCHEMA_FILES:

        logging.error(
            f"Version {checker_data.schema_version} unsupported. Checker {parameters_constants.CHECKER_ID} skipped"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=parameters_constants.CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    rule_list = [valid_parameter_declaration_in_catalogs.check_rule]

    for rule in rule_list:
        rule(checker_data=checker_data)

    logging.info(
        f"Issues found - {checker_data.result.get_checker_issue_count(checker_bundle_name=constants.BUNDLE_NAME, checker_id=parameters_constants.CHECKER_ID)}"
    )

    # TODO: Add logic to deal with error or to skip it
    checker_data.result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=parameters_constants.CHECKER_ID,
        status=StatusType.COMPLETED,
    )
