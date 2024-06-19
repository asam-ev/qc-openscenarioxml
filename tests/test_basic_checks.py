import os
import pytest
import test_utils
from qc_openscenario import constants
from qc_openscenario.checks.basic_checker import basic_constants
from qc_baselib import Result, IssueSeverity


def test_valid_xml_document_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_xml_document/"
    target_file_name = f"xml.valid_xml_document.positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(result.get_issues_by_rule_uid("asam.net:xosc:1.0.0:xml.valid_xml_document"))
        == 0
    )

    test_utils.cleanup_files()


def test_valid_xml_document_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_xml_document/"
    target_file_name = f"xml.valid_xml_document.negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    xml_doc_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.0.0:xml.valid_xml_document"
    )
    assert len(xml_doc_issues) == 1
    assert xml_doc_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()
