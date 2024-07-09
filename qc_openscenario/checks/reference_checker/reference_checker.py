import logging

from lxml import etree

from qc_baselib import Configuration, Result, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.reference_checker import (
    reference_constants,
    uniquely_resolvable_entity_references,
    resolvable_signal_id_in_traffic_signal_state_action,
    resolvable_traffic_signal_controller_by_traffic_signal_controller_ref,
)


def run_checks(checker_data: models.CheckerData) -> None:
    logging.info("Executing reference checks")

    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
        description="Check if xml properties of input file are properly set",
        summary="",
    )

    # Skip if basic checks fail
    if checker_data.input_file_xml_root is None:
        logging.error(
            f"Invalid xml input file. Checker {reference_constants.CHECKER_ID} skipped"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=reference_constants.CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    # Skip if schema checks are skipped
    if (
        checker_data.result.get_checker_result("xoscBundle", "schema_xosc").status
        is StatusType.SKIPPED
    ):
        logging.error(
            f"Schema checks have been skipped. Checker {reference_constants.CHECKER_ID} skipped"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=reference_constants.CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    rule_list = [
        uniquely_resolvable_entity_references.check_rule,
        resolvable_signal_id_in_traffic_signal_state_action.check_rule,
        resolvable_traffic_signal_controller_by_traffic_signal_controller_ref.check_rule,
    ]

    for rule in rule_list:
        rule(checker_data=checker_data)

    logging.info(
        f"Issues found - {checker_data.result.get_checker_issue_count(checker_bundle_name=constants.BUNDLE_NAME, checker_id=reference_constants.CHECKER_ID)}"
    )

    # TODO: Add logic to deal with error or to skip it
    checker_data.result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
        status=StatusType.COMPLETED,
    )
