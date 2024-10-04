import os
import pytest
import test_utils
from qc_baselib import Result, IssueSeverity, StatusType
from qc_openscenario.checks import basic_checker


def test_non_existing_road_network_file(
    monkeypatch,
) -> None:
    base_path = "tests/data/non_existing_road_network_file/"
    target_file_name = f"non_existing_road_network_file.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    # Should have no exception
    assert True
    test_utils.cleanup_files()
