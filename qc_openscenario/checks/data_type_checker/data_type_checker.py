import logging

from qc_openscenario.checks import models

from qc_openscenario.checks.data_type_checker import (
    allowed_operators,
    non_negative_transition_time_in_light_state_action,
    positive_duration_in_phase,
)


def run_checks(checker_data: models.CheckerData) -> None:
    logging.info("Executing data_type checks")

    allowed_operators.check_rule(checker_data)
    non_negative_transition_time_in_light_state_action.check_rule(checker_data)
    positive_duration_in_phase.check_rule(checker_data)
