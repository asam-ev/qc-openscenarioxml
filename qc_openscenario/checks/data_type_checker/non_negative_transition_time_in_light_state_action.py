import logging

from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = (
    "check_asam_xosc_data_type_non_negative_transition_time_in_light_state_action"
)
CHECKER_DESCRIPTION = "Expressions in OpenSCENARIO must only use the allowed operands."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = (
    "asam.net:xosc:1.2.0:data_type.non_negative_transition_time_in_light_state_action"
)


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xosc:1.2.0:data_type.non_negative_transition_time_in_light_state_action

    Description: transitionTime in LightStateAction should be non-negative
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/32
    """
    logging.info("Executing non_negative_transition_time_in_light_state_action check")

    root = checker_data.input_file_xml_root

    light_state_nodes = root.findall(".//LightStateAction")

    for light_state_node in light_state_nodes:
        current_transition_time = light_state_node.get("transitionTime")
        if current_transition_time is None:
            continue

        current_transition_type = utils.get_attribute_type(current_transition_time)
        logging.debug(f"current_transition_type: {current_transition_type}")
        if current_transition_type == models.AttributeType.EXPRESSION:
            logging.debug(
                f"Skipping transitionTime with value {current_transition_time} since sign cannot be evaluated "
            )
            continue
        if current_transition_type == models.AttributeType.PARAMETER:
            current_transition_param_name = current_transition_time[1:]
            current_transition_param_value = utils.get_parameter_value_from_node(
                root, light_state_node, current_transition_param_name
            )
            logging.debug(
                f"current_transition_param_name: {current_transition_param_name}"
            )
            logging.debug(
                f"current_transition_param_name: {current_transition_param_name}"
            )
            # Parameter value is assigned to the current_transition_time to search
            # If parameter is not found, None is assigned to current_transition_time
            if current_transition_param_value is None:
                continue
            current_transition_time = current_transition_param_value
        # Case of incomplete expression to skip
        if (
            current_transition_type == models.AttributeType.VALUE
            and current_transition_time.startswith("$")
        ):
            continue

        logging.debug(f"current_transition_time: {current_transition_time}")
        if not utils.is_xsd_double(current_transition_time):
            logging.error(
                f"Cannot convert '{current_transition_time}' to double as it does not match xsd:double pattern. Skipping check..."
            )

            checker_data.result.set_checker_status(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                status=StatusType.SKIPPED,
            )

            return

        current_numeric_value = utils.to_float(current_transition_time)

        if current_numeric_value is None:
            continue

        has_issue = current_numeric_value < 0

        if has_issue:
            xpath = root.getpath(light_state_node)

            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="Issue transitionTime in LightStateAction node is negative",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"transitionTime duration {current_numeric_value} is negative",
            )
