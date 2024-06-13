import os
import pytest
import test_utils
from qc_openscenario import constants
from qc_openscenario.checks.schema_checker import schema_constants
from qc_baselib import Result, IssueSeverity


def test_schema_is_valid_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/schema_is_valid/"
    target_file_name = f"xml.schema_is_valid.positive.xml"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    checker_result = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=schema_constants.CHECKER_ID,
    )
    assert (
        len(test_utils.get_issues_by_rule_name(checker_result, "xml.schema_is_valid"))
        == 0
    )
    test_utils.cleanup_files()


def test_schema_is_valid_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/schema_is_valid/"
    target_file_name = f"xml.schema_is_valid.negative.xml"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    checker_result = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=schema_constants.CHECKER_ID,
    )
    assert (
        len(test_utils.get_issues_by_rule_name(checker_result, "xml.schema_is_valid"))
        == 0
    )
    test_utils.cleanup_files()


def test_unsupported_schema_version(
    monkeypatch,
) -> None:
    base_path = "tests/data/schema_is_valid/"
    target_file_name = f"test_ramp_v09.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    checker_result = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=schema_constants.CHECKER_ID,
    )
    assert (
        len(test_utils.get_issues_by_rule_name(checker_result, "xml.schema_is_valid"))
        == 0
    )
    test_utils.cleanup_files()


def test_invalid_schema(
    monkeypatch,
) -> None:
    base_path = "tests/data/schema_is_valid/"
    target_file_name = f"invalid_schema.xml"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    checker_result = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=schema_constants.CHECKER_ID,
    )

    xml_schema_issues = test_utils.get_issues_by_rule_name(
        checker_result, "xml.schema_is_valid"
    )
    assert len(xml_schema_issues) == 1
    assert xml_schema_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()
