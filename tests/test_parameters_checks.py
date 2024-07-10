import os
import pytest
import test_utils
from qc_openscenario import constants
from qc_openscenario.checks.parameters_checker import parameters_constants
from qc_baselib import Result, IssueSeverity


def test_valid_parameter_declaration_in_catalogs_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_parameter_declaration_in_catalogs/"
    target_file_name = (
        f"parameters.valid_parameter_declaration_in_catalogs.positive.xosc"
    )
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:parameters.valid_parameter_declaration_in_catalogs"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_valid_parameter_declaration_in_catalogs_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_parameter_declaration_in_catalogs/"
    target_file_name = (
        f"parameters.valid_parameter_declaration_in_catalogs.negative.xosc"
    )
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=parameters_constants.CHECKER_ID,
    )

    parameters_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:parameters.valid_parameter_declaration_in_catalogs"
    )
    assert len(parameters_issues) == 1
    assert parameters_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_valid_parameter_declaration_in_catalogs_negative_no_default(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_parameter_declaration_in_catalogs/"
    target_file_name = (
        f"parameters.valid_parameter_declaration_in_catalogs.negative_no_default.xosc"
    )
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=parameters_constants.CHECKER_ID,
    )

    parameters_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:parameters.valid_parameter_declaration_in_catalogs"
    )
    assert len(parameters_issues) == 1
    assert parameters_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_valid_parameter_declaration_in_catalogs_negative_multiple(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_parameter_declaration_in_catalogs/"
    target_file_name = (
        f"parameters.valid_parameter_declaration_in_catalogs.negative.multiple.xosc"
    )
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=parameters_constants.CHECKER_ID,
    )

    parameters_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:parameters.valid_parameter_declaration_in_catalogs"
    )
    assert len(parameters_issues) == 2
    assert parameters_issues[0].level == IssueSeverity.ERROR
    assert parameters_issues[1].level == IssueSeverity.ERROR
    assert "maxSteering" in parameters_issues[0].locations[0].description
    assert "trackWidth" in parameters_issues[1].locations[0].description
    test_utils.cleanup_files()
