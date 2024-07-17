import os
import pytest
import test_utils
from qc_openscenario import constants
from qc_openscenario.checks.data_type_checker import data_type_constants
from qc_baselib import Result, IssueSeverity


def test_positive_duration_in_phase_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/positive_duration_in_phase/"
    target_file_name = f"positive_example.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:data_type.positive_duration_in_phase"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_positive_duration_in_phase_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/positive_duration_in_phase/"
    target_file_name = f"negative_example.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=data_type_constants.CHECKER_ID,
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.positive_duration_in_phase"
    )
    assert len(data_type_issues) == 1
    assert data_type_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_allowed_operators_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/allowed_operators/"
    target_file_name = f"positive_example.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:data_type.allowed_operators"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_allowed_operators_positive_multiple(
    monkeypatch,
) -> None:
    base_path = "tests/data/allowed_operators/"
    target_file_name = f"positive_example_multiple.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:data_type.allowed_operators"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_allowed_operators_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/allowed_operators/"
    target_file_name = f"negative_example.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=data_type_constants.CHECKER_ID,
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.allowed_operators"
    )
    assert len(data_type_issues) == 1
    assert data_type_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_allowed_operators_negative_typo(
    monkeypatch,
) -> None:
    base_path = "tests/data/allowed_operators/"
    target_file_name = f"negative_example_typo.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=data_type_constants.CHECKER_ID,
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.allowed_operators"
    )
    assert len(data_type_issues) == 1
    assert data_type_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_allowed_operators_negative_multiple(
    monkeypatch,
) -> None:
    base_path = "tests/data/allowed_operators/"
    target_file_name = f"negative_example_multiple.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=data_type_constants.CHECKER_ID,
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.allowed_operators"
    )
    assert len(data_type_issues) == 4
    assert data_type_issues[0].level == IssueSeverity.ERROR
    assert data_type_issues[1].level == IssueSeverity.ERROR
    assert data_type_issues[2].level == IssueSeverity.ERROR
    assert "}" in data_type_issues[0].locations[0].description
    assert "powerer" in data_type_issues[1].locations[0].description
    assert "^" in data_type_issues[2].locations[0].description
    assert "^" in data_type_issues[3].locations[0].description
    test_utils.cleanup_files()


def test_non_negative_transition_time_in_light_state_action_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/transition_time_should_be_non_negative/"
    target_file_name = f"positive_example.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:data_type.non_negative_transition_time_in_light_state_action"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_non_negative_transition_time_in_light_state_action_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/transition_time_should_be_non_negative/"
    target_file_name = f"negative_example.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=data_type_constants.CHECKER_ID,
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.non_negative_transition_time_in_light_state_action"
    )
    assert len(data_type_issues) == 1
    assert data_type_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_non_negative_transition_time_in_light_state_action_negative_param(
    monkeypatch,
) -> None:
    base_path = "tests/data/transition_time_should_be_non_negative/"
    target_file_name = f"negative_example_param.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=data_type_constants.CHECKER_ID,
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.non_negative_transition_time_in_light_state_action"
    )
    assert len(data_type_issues) == 1
    assert data_type_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()
