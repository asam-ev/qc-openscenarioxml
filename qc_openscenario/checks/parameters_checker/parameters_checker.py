import logging
from qc_openscenario.checks import models
from qc_openscenario.checks.parameters_checker import (
    valid_parameter_declaration_in_catalogs,
)


def run_checks(checker_data: models.CheckerData) -> None:
    logging.info("Executing parameters checks")
    valid_parameter_declaration_in_catalogs.check_rule(checker_data)
