import logging

from lxml import etree

from qc_baselib import Configuration, Result, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models
from qc_openscenario.schema import schema_files

from qc_openscenario.checks.data_type_checker import (
    data_type_constants,
    allowed_operators,
    non_negative_transition_time_in_light_state_action,
    positive_duration_in_phase,
)


def run_checks(checker_data: models.CheckerData) -> None:
    logging.info("Executing data_type checks")

    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=data_type_constants.CHECKER_ID,
        description="Check if data_type properties of input file are properly set",
        summary="",
    )

    if checker_data.input_file_xml_root is None:
        logging.error(
            f"Invalid xml input file. Checker {data_type_constants.CHECKER_ID} skipped"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=data_type_constants.CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    if checker_data.schema_version not in schema_files.SCHEMA_FILES:

        logging.error(
            f"Version {checker_data.schema_version} unsupported. Checker {data_type_constants.CHECKER_ID} skipped"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=data_type_constants.CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    rule_list = [
        allowed_operators.check_rule,
        non_negative_transition_time_in_light_state_action.check_rule,
        positive_duration_in_phase.check_rule,
    ]

    for rule in rule_list:
        rule(checker_data=checker_data)

    logging.info(
        f"Issues found - {checker_data.result.get_checker_issue_count(checker_bundle_name=constants.BUNDLE_NAME, checker_id=data_type_constants.CHECKER_ID)}"
    )

    # TODO: Add logic to deal with error or to skip it
    checker_data.result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=data_type_constants.CHECKER_ID,
        status=StatusType.COMPLETED,
    )
