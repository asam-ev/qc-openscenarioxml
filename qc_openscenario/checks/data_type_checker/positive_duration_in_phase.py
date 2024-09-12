import logging

from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.data_type_checker import data_type_checker_precondition

CHECKER_ID = "check_asam_xosc_positive_duration_in_phase"
MIN_RULE_VERSION = "1.2.0"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xosc:1.2.0:data_type.positive_duration_in_phase

    Description: Attribute “duration” in the complex type “Phase” (e.g., for TrafficSignalController”) shall be non-negative.
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/33
    """
    logging.info("Executing positive_duration_in_phase check")

    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        description="Expressions in OpenSCENARIO must only use the allowed operands.",
    )

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting=MIN_RULE_VERSION,
        rule_full_name="data_type.positive_duration_in_phase",
    )

    if not checker_data.result.all_checkers_completed_without_issue(
        data_type_checker_precondition.PRECONDITIONS
    ):
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        return

    schema_version = checker_data.schema_version
    if (
        schema_version is None
        or utils.compare_versions(schema_version, MIN_RULE_VERSION) < 0
    ):
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        return

    root = checker_data.input_file_xml_root

    phase_nodes = root.findall(".//Phase")

    for phase_node in phase_nodes:
        current_duration = phase_node.get("duration")
        logging.debug(f"current_duration: {current_duration}")
        current_duration_type = utils.get_attribute_type(current_duration)

        if current_duration is None:
            continue
        if current_duration_type == models.AttributeType.EXPRESSION:
            logging.debug(
                f"Skipping duration with value {current_duration} since sign cannot be evaluated "
            )
            continue
        if current_duration_type == models.AttributeType.PARAMETER:
            current_duration_param_name = current_duration[1:]
            current_duration_param_value = utils.get_parameter_value_from_node(
                root, phase_node, current_duration_param_name
            )
            logging.debug(f"current_duration_param_name: {current_duration_param_name}")
            logging.debug(
                f"current_duration_param_value: {current_duration_param_value}"
            )
            # Parameter value is assigned to the current_duration to search
            # If parameter is not found, None is assigned to current_duration
            if current_duration_param_value is None:
                continue
            current_duration = current_duration_param_value

        if not utils.is_xsd_double(current_duration):
            logging.error(
                f"Cannot convert '{current_duration}' to double as it does not match xsd:double pattern. Skipping check..."
            )

            checker_data.result.set_checker_status(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                status=StatusType.SKIPPED,
            )

            return

        current_numeric_value = float(current_duration)
        has_issue = current_numeric_value < 0

        if has_issue:
            xpath = root.getpath(phase_node)

            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="Issue flagging when attribute “duration” in the complex type “Phase” is negative",
                level=IssueSeverity.ERROR,
                rule_uid=rule_uid,
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"Phase duration {current_numeric_value} is negative",
            )

    checker_data.result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        status=StatusType.COMPLETED,
    )
