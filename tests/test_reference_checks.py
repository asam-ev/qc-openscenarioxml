import os
import pytest
import test_utils
from qc_openscenario import constants
from qc_openscenario.checks.reference_checker import reference_constants
from qc_baselib import Result, IssueSeverity


def test_uniquely_resolvable_positive1(
    monkeypatch,
) -> None:
    base_path = "tests/data/uniquely_resolvable_entity_references/"
    target_file_name = f"vehicle_catalog_positive1.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
    )
    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.uniquely_resolvable_entity_references"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_uniquely_resolvable_positive2(
    monkeypatch,
) -> None:
    base_path = "tests/data/uniquely_resolvable_entity_references/"
    target_file_name = f"vehicle_catalog_positive2.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
    )
    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.uniquely_resolvable_entity_references"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_uniquely_resolvable_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/uniquely_resolvable_entity_references/"
    target_file_name = f"vehicle_catalog_negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.uniquely_resolvable_entity_references"
    )
    assert len(reference_issues) == 1
    assert reference_issues[0].level == IssueSeverity.WARNING
    test_utils.cleanup_files()


def test_long_catalog_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/uniquely_resolvable_entity_references/"
    target_file_name = f"long_catalog_negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
    )
    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.uniquely_resolvable_entity_references"
    )
    assert len(reference_issues) == 1
    assert reference_issues[0].level == IssueSeverity.WARNING
    test_utils.cleanup_files()


def test_long_catalog_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/uniquely_resolvable_entity_references/"
    target_file_name = f"long_catalog_positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
    )
    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.uniquely_resolvable_entity_references"
            )
        )
        == 0
    )


def test_minimum_version(
    monkeypatch,
) -> None:
    base_path = "tests/data/uniquely_resolvable_entity_references/"
    target_file_name = f"vehicle_catalog_negative_v10.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
    )
    # 0 issues because minumum version is not met and the check is not performed
    # (even if it is a negative sample)
    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.uniquely_resolvable_entity_references"
            )
        )
        == 0
    )


def test_traffic_signal_state_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_signal_id_in_traffic_signal_state_action/"
    target_file_name = f"reference_control.resolvable_signal_id_in_traffic_signal_state_action.positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
    )
    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.resolvable_signal_id_in_traffic_signal_state_action"
            )
        )
        == 0
    )


def test_traffic_signal_state_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_signal_id_in_traffic_signal_state_action/"
    target_file_name = f"reference_control.resolvable_signal_id_in_traffic_signal_state_action.negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
    )

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.resolvable_signal_id_in_traffic_signal_state_action"
    )
    assert len(reference_issues) == 1
    assert reference_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_traffic_signal_controller_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_traffic_signal_controller_by_traffic_signal_controller_ref/"
    target_file_name = f"reference_control.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref.positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
    )
    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref"
            )
        )
        == 0
    )


def test_traffic_signal_controller_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_traffic_signal_controller_by_traffic_signal_controller_ref/"
    target_file_name = f"reference_control.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref.negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
    )

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref"
    )
    assert len(reference_issues) == 1
    assert reference_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_traffic_signal_controller_multiple_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_traffic_signal_controller_by_traffic_signal_controller_ref/"
    target_file_name = f"reference_control.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref.negative.multiple.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    _ = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=reference_constants.CHECKER_ID,
    )

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref"
    )
    assert len(reference_issues) == 2
    assert reference_issues[0].level == IssueSeverity.ERROR
    assert reference_issues[1].level == IssueSeverity.ERROR
    assert "bar" in reference_issues[0].locations[0].description
    assert "0000" in reference_issues[1].locations[0].description
    test_utils.cleanup_files()
