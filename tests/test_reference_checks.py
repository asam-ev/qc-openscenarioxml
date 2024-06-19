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
