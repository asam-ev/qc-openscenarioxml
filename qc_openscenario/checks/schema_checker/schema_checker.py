import logging


from qc_openscenario.checks import models

from qc_openscenario.checks.schema_checker import (
    valid_schema,
)


def run_checks(checker_data: models.CheckerData) -> None:
    logging.info("Executing schema checks")
    valid_schema.check_rule(checker_data)
