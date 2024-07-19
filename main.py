import argparse
import logging
from datetime import datetime

from qc_baselib import Configuration, Result

from qc_openscenario import constants
from qc_openscenario.checks.schema_checker import schema_checker
from qc_openscenario.checks.basic_checker import basic_checker
from qc_openscenario.checks.reference_checker import reference_checker
from qc_openscenario.checks.parameters_checker import parameters_checker
from qc_openscenario.checks.data_type_checker import data_type_checker

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def args_entrypoint() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="QC OpenScenario Checker",
        description="This is a collection of scripts for checking validity of OpenScenario (.xosc) files.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--default_config", action="store_true")
    group.add_argument("-c", "--config_path")

    return parser.parse_args()


def main():
    args = args_entrypoint()

    logging.info("Initializing checks")

    if args.default_config:
        raise RuntimeError("Not implemented.")
    else:
        config = Configuration()
        config.load_from_file(xml_file_path=args.config_path)

        result = Result()
        result.register_checker_bundle(
            name=constants.BUNDLE_NAME,
            build_date=datetime.today().strftime("%Y-%m-%d"),
            description="OpenScenario checker bundle",
            version=constants.BUNDLE_VERSION,
            summary="",
        )
        result.set_result_version(version=constants.BUNDLE_VERSION)

        # 1. Run basic checks
        checker_data = basic_checker.run_checks(config=config, result=result)

        # 2. Run xml checks
        schema_checker.run_checks(checker_data)

        # 3. Run reference checks
        reference_checker.run_checks(checker_data)

        # 4. Run parameters checks
        parameters_checker.run_checks(checker_data)

        # 5. Run data_type checks
        data_type_checker.run_checks(checker_data)

        result.write_to_file(
            config.get_checker_bundle_param(
                checker_bundle_name=constants.BUNDLE_NAME, param_name="resultFile"
            )
        )

    logging.info("Done")


if __name__ == "__main__":
    main()
