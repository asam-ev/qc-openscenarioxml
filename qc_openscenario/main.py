import argparse
import logging
from datetime import datetime
import types

from qc_baselib import Configuration, Result, StatusType
from qc_baselib.models.common import ParamType

from qc_openscenario import constants
from qc_openscenario.checks import schema_checker
from qc_openscenario.checks import basic_checker
from qc_openscenario.checks import reference_checker
from qc_openscenario.checks import parameters_checker
from qc_openscenario.checks import data_type_checker
from qc_openscenario.checks import utils, models

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def args_entrypoint() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="QC OpenScenario Checker",
        description="This is a collection of scripts for checking validity of OpenScenario (.xosc) files.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--default_config", action="store_true")
    group.add_argument("-c", "--config_path")

    parser.add_argument("-g", "--generate_markdown", action="store_true")

    return parser.parse_args()


def execute_checker(
    checker: types.ModuleType,
    checker_data: models.CheckerData,
    required_definition_setting: bool = True,
) -> None:
    # Register checker
    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=checker.CHECKER_ID,
        description=checker.CHECKER_DESCRIPTION,
    )

    # Register rule uid
    checker_data.result.register_rule_by_uid(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=checker.CHECKER_ID,
        rule_uid=checker.RULE_UID,
    )

    # Check preconditions. If not satisfied then set status as SKIPPED and return
    if not checker_data.result.all_checkers_completed_without_issue(
        checker.CHECKER_PRECONDITIONS
    ):
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=checker.CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            checker.CHECKER_ID,
            "Preconditions are not satisfied. Skip the check.",
        )

        return

    # Checker definition setting. If not satisfied then set status as SKIPPED and return
    if required_definition_setting:
        schema_version = checker_data.schema_version

        splitted_rule_uid = checker.RULE_UID.split(":")
        if len(splitted_rule_uid) != 4:
            raise RuntimeError(f"Invalid rule uid: {checker.RULE_UID}")

        definition_setting = splitted_rule_uid[2]
        if (
            schema_version is None
            or utils.compare_versions(schema_version, definition_setting) < 0
        ):
            checker_data.result.set_checker_status(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=checker.CHECKER_ID,
                status=StatusType.SKIPPED,
            )

            checker_data.result.add_checker_summary(
                constants.BUNDLE_NAME,
                checker.CHECKER_ID,
                f"Version {schema_version} is lower than definition setting {definition_setting}. Skip the check.",
            )

            return

    # Execute checker
    try:
        checker.check_rule(checker_data)

        # If checker is not explicitly set as SKIPPED, then set it as COMPLETED
        if (
            checker_data.result.get_checker_status(checker.CHECKER_ID)
            != StatusType.SKIPPED
        ):
            checker_data.result.set_checker_status(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=checker.CHECKER_ID,
                status=StatusType.COMPLETED,
            )
    except Exception as e:
        # If any exception occurs during the check, set the status as ERROR
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=checker.CHECKER_ID,
            status=StatusType.ERROR,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME, checker.CHECKER_ID, f"Error: {str(e)}."
        )

        logging.exception(f"An error occurred in {checker.CHECKER_ID}.")


def run_checks(config: Configuration, result: Result) -> None:
    checker_data = models.CheckerData(
        xml_file_path=config.get_config_param("InputFile"),
        input_file_xml_root=None,
        config=config,
        result=result,
        schema_version=None,
        xodr_root=None,
    )

    # 1. Run basic checks
    execute_checker(
        basic_checker.valid_xml_document,
        checker_data,
        required_definition_setting=False,
    )

    if result.all_checkers_completed_without_issue(
        {basic_checker.valid_xml_document.CHECKER_ID}
    ):
        checker_data.input_file_xml_root = utils.get_root_without_default_namespace(
            checker_data.xml_file_path
        )

    execute_checker(
        basic_checker.root_tag_is_openscenario,
        checker_data,
        required_definition_setting=False,
    )
    execute_checker(
        basic_checker.fileheader_is_present,
        checker_data,
        required_definition_setting=False,
    )
    execute_checker(
        basic_checker.version_is_defined,
        checker_data,
        required_definition_setting=False,
    )

    # Get schema version and xodr road network if they exist
    if result.all_checkers_completed_without_issue(
        {
            basic_checker.valid_xml_document.CHECKER_ID,
            basic_checker.root_tag_is_openscenario.CHECKER_ID,
            basic_checker.fileheader_is_present.CHECKER_ID,
            basic_checker.version_is_defined.CHECKER_ID,
        }
    ):
        checker_data.schema_version = utils.get_standard_schema_version(
            checker_data.input_file_xml_root
        )
        checker_data.xodr_root = utils.get_xodr_road_network(
            checker_data.xml_file_path, checker_data.input_file_xml_root
        )

    # 2. Run schema check
    execute_checker(schema_checker.valid_schema, checker_data)

    # 3. Run reference checks
    execute_checker(
        reference_checker.uniquely_resolvable_entity_references, checker_data
    )
    execute_checker(
        reference_checker.resolvable_signal_id_in_traffic_signal_state_action,
        checker_data,
    )
    execute_checker(
        reference_checker.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref,
        checker_data,
    )
    execute_checker(
        reference_checker.valid_actor_reference_in_private_actions, checker_data
    )
    execute_checker(reference_checker.resolvable_entity_references, checker_data)
    execute_checker(reference_checker.resolvable_variable_reference, checker_data)
    execute_checker(
        reference_checker.resolvable_storyboard_element_reference, checker_data
    )
    execute_checker(reference_checker.unique_element_names_on_same_level, checker_data)

    # 4. Run parameters checks
    execute_checker(
        parameters_checker.valid_parameter_declaration_in_catalogs, checker_data
    )

    # 5. Run data_type checks
    execute_checker(data_type_checker.allowed_operators, checker_data)
    execute_checker(
        data_type_checker.non_negative_transition_time_in_light_state_action,
        checker_data,
    )
    execute_checker(data_type_checker.positive_duration_in_phase, checker_data)


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
            description="OpenScenario checker bundle",
            version=constants.BUNDLE_VERSION,
            summary="",
        )
        result.set_result_version(version=constants.BUNDLE_VERSION)

        run_checks(config, result)

        result.copy_param_from_config(config)

        result.write_to_file(
            config.get_checker_bundle_param(
                checker_bundle_name=constants.BUNDLE_NAME, param_name="resultFile"
            ),
            generate_summary=True,
        )

        if args.generate_markdown:
            result.write_markdown_doc("generated_checker_bundle_doc.md")

    logging.info("Done")


if __name__ == "__main__":
    main()
