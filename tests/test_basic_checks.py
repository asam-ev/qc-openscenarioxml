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


def test_parametric_input_xodr(
    monkeypatch,
) -> None:
    base_path = "tests/data/parametric_input_xodr/"
    target_file_name = f"CloseVehicleCrossing.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert result.get_issue_count() == 0
    test_utils.cleanup_files()


def test_parametric_entity_ref(
    monkeypatch,
) -> None:
    base_path = "tests/data/parametric_entity_ref/"
    target_file_name = f"CutIn.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert result.get_issue_count() == 0
    test_utils.cleanup_files()


def test_parameter_declaration_with_expression(
    monkeypatch,
) -> None:
    base_path = "tests/data/parameter_declaration_with_expression/"
    target_file_name = f"VehicleCatalog.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert result.get_issue_count() == 0
    test_utils.cleanup_files()


def test_root_tag_is_openscenario_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/root_tag_is_openscenario/"
    target_file_name = f"positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.0.0:xml.root_tag_is_openscenario"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_root_tag_is_openscenario_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/root_tag_is_openscenario/"
    target_file_name = f"negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    xml_doc_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.0.0:xml.root_tag_is_openscenario"
    )
    assert len(xml_doc_issues) == 1
    assert xml_doc_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_fileheader_is_present_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/fileheader_is_present/"
    target_file_name = f"positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.0.0:xml.fileheader_is_present"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_fileheader_is_present_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/fileheader_is_present/"
    target_file_name = f"negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    xml_doc_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.0.0:xml.fileheader_is_present"
    )
    assert len(xml_doc_issues) == 1
    assert xml_doc_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_version_is_defined__positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/version_is_defined/"
    target_file_name = f"positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(result.get_issues_by_rule_uid("asam.net:xosc:1.0.0:xml.version_is_defined"))
        == 0
    )

    test_utils.cleanup_files()


def test_version_is_defined_negative_attr(
    monkeypatch,
) -> None:
    base_path = "tests/data/version_is_defined/"
    target_file_name = f"negative_no_attr.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    xml_doc_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.0.0:xml.version_is_defined"
    )
    assert len(xml_doc_issues) == 1
    assert xml_doc_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_version_is_defined_negative_type(
    monkeypatch,
) -> None:
    base_path = "tests/data/version_is_defined/"
    target_file_name = f"negative_no_type.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    xml_doc_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.0.0:xml.version_is_defined"
    )
    assert len(xml_doc_issues) == 1
    assert xml_doc_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()
