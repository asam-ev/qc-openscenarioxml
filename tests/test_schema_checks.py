import os
import pytest
import test_utils
from qc_openscenario import constants
from qc_openscenario.checks.schema_checker import schema_constants
from qc_baselib import Result, IssueSeverity


def test_valid_schema_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_schema/"
    target_file_name = f"xml.valid_schema.positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(result.get_issues_by_rule_uid("asam.net:xosc:1.0.0:xml.valid_schema"))
        == 0
    )

    test_utils.cleanup_files()


def test_valid_schema_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_schema/"
    target_file_name = f"xml.valid_schema.negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(result.get_issues_by_rule_uid("asam.net:xosc:1.0.0:xml.valid_schema"))
        == 0
    )
    test_utils.cleanup_files()


def test_unsupported_schema_version(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_schema/"
    target_file_name = f"unsupported_schema.xosc"
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
        len(result.get_issues_by_rule_uid("asam.net:xosc:1.0.0:xml.valid_schema"))
        == 0
    )
    test_utils.cleanup_files()


def test_invalid_schema(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_schema/"
    target_file_name = f"invalid_schema.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    checker_result = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=schema_constants.CHECKER_ID,
    )

    xml_schema_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.0.0:xml.valid_schema"
    )
    assert len(xml_schema_issues) == 1
    assert xml_schema_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()
