import logging


from qc_baselib import StatusType

from qc_openscenario import constants
from qc_openscenario.checks import models

from qc_openscenario.checks.schema_checker import valid_schema

from qc_openscenario.checks.reference_checker import (
    uniquely_resolvable_entity_references,
    resolvable_signal_id_in_traffic_signal_state_action,
    resolvable_traffic_signal_controller_by_traffic_signal_controller_ref,
    valid_actor_reference_in_private_actions,
    resolvable_entity_references,
    resolvable_variable_reference,
    resolvable_storyboard_element_reference,
    unique_element_names_on_same_level,
)


def run_checks(checker_data: models.CheckerData) -> None:
    logging.info("Executing reference checks")

    uniquely_resolvable_entity_references.check_rule(checker_data=checker_data)
    resolvable_signal_id_in_traffic_signal_state_action.check_rule(
        checker_data=checker_data
    )
    resolvable_traffic_signal_controller_by_traffic_signal_controller_ref.check_rule(
        checker_data=checker_data
    )
    valid_actor_reference_in_private_actions.check_rule(checker_data=checker_data)
    resolvable_entity_references.check_rule(checker_data=checker_data)
    resolvable_variable_reference.check_rule(checker_data=checker_data)
    resolvable_storyboard_element_reference.check_rule(checker_data=checker_data)
    unique_element_names_on_same_level.check_rule(checker_data=checker_data)
