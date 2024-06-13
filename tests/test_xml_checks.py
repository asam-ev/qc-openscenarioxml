import os
import sys
import pytest

from typing import List

import main

from qc_openscenario import constants, checks
from qc_openscenario.checks.xml_checker import xml_constants

from qc_baselib import Configuration, Result, IssueSeverity

CONFIG_FILE_PATH = "bundle_config.xml"
REPORT_FILE_PATH = "xosc_bundle_report.xqar"


def create_test_config(target_file_path: str):
    test_config = Configuration()
    test_config.set_config_param(name="XoscFile", value=target_file_path)
    test_config.register_checker_bundle(checker_bundle_name=constants.BUNDLE_NAME)
    test_config.set_checker_bundle_param(
        checker_bundle_name=constants.BUNDLE_NAME,
        name="resultFile",
        value=REPORT_FILE_PATH,
    )

    test_config.write_to_file(CONFIG_FILE_PATH)


def launch_main(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "-c",
            CONFIG_FILE_PATH,
        ],
    )
    main.main()


def cleanup_files():
    os.remove(REPORT_FILE_PATH)
    os.remove(CONFIG_FILE_PATH)


def test_is_an_xml_document_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/is_an_xml_document/"
    target_file_name = f"xml.is_an_xml_document.positive.xml"
    target_file_path = os.path.join(base_path, target_file_name)

    create_test_config(target_file_path)

    launch_main(monkeypatch)

    result = Result()
    result.load_from_file(REPORT_FILE_PATH)

    checker_result = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=xml_constants.CHECKER_ID,
    )
    assert len(checker_result.issues) == 0
    cleanup_files()


def test_is_an_xml_document_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/is_an_xml_document/"
    target_file_name = f"xml.is_an_xml_document.negative.xml"
    target_file_path = os.path.join(base_path, target_file_name)

    create_test_config(target_file_path)

    launch_main(monkeypatch)

    result = Result()
    result.load_from_file(REPORT_FILE_PATH)

    checker_result = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=xml_constants.CHECKER_ID,
    )
    assert len(checker_result.issues) == 1
    cleanup_files()


def test_schema_is_valid_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/schema_is_valid/"
    target_file_name = f"xml.schema_is_valid.positive.xml"
    target_file_path = os.path.join(base_path, target_file_name)

    create_test_config(target_file_path)

    launch_main(monkeypatch)

    result = Result()
    result.load_from_file(REPORT_FILE_PATH)

    checker_result = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=xml_constants.CHECKER_ID,
    )
    assert len(checker_result.issues) == 0
    cleanup_files()


def test_schema_is_valid_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/schema_is_valid/"
    target_file_name = f"xml.schema_is_valid.negative.xml"
    target_file_path = os.path.join(base_path, target_file_name)

    create_test_config(target_file_path)

    launch_main(monkeypatch)

    result = Result()
    result.load_from_file(REPORT_FILE_PATH)

    checker_result = result.get_checker_result(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=xml_constants.CHECKER_ID,
    )
    assert len(checker_result.issues) == 1
    cleanup_files()
