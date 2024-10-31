# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import pytest
import test_utils
from qc_baselib import Result, IssueSeverity, StatusType
from qc_openscenario.checks import reference_checker


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

    assert (
        result.get_checker_status(
            reference_checker.uniquely_resolvable_entity_references.CHECKER_ID
        )
        == StatusType.COMPLETED
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

    assert (
        result.get_checker_status(
            reference_checker.uniquely_resolvable_entity_references.CHECKER_ID
        )
        == StatusType.COMPLETED
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

    assert (
        result.get_checker_status(
            reference_checker.uniquely_resolvable_entity_references.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

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

    assert (
        result.get_checker_status(
            reference_checker.uniquely_resolvable_entity_references.CHECKER_ID
        )
        == StatusType.COMPLETED
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

    assert (
        result.get_checker_status(
            reference_checker.uniquely_resolvable_entity_references.CHECKER_ID
        )
        == StatusType.COMPLETED
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

    assert (
        result.get_checker_status(
            reference_checker.uniquely_resolvable_entity_references.CHECKER_ID
        )
        == StatusType.SKIPPED
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

    assert (
        result.get_checker_status(
            reference_checker.resolvable_signal_id_in_traffic_signal_state_action.CHECKER_ID
        )
        == StatusType.COMPLETED
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

    assert (
        result.get_checker_status(
            reference_checker.resolvable_signal_id_in_traffic_signal_state_action.CHECKER_ID
        )
        == StatusType.COMPLETED
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

    assert (
        result.get_checker_status(
            reference_checker.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref.CHECKER_ID
        )
        == StatusType.COMPLETED
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

    assert (
        result.get_checker_status(
            reference_checker.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref.CHECKER_ID
        )
        == StatusType.COMPLETED
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

    assert (
        result.get_checker_status(
            reference_checker.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref.CHECKER_ID
        )
        == StatusType.COMPLETED
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


def test_valid_actor_reference_in_private_actions_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_actor_reference_in_private_actions/"
    target_file_name = (
        f"reference_control.valid_actor_reference_in_private_actions.positive.xosc"
    )
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.valid_actor_reference_in_private_actions.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.valid_actor_reference_in_private_actions"
            )
        )
        == 0
    )


def test_valid_actor_reference_in_private_actions_positive_with_entity(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_actor_reference_in_private_actions/"
    target_file_name = f"reference_control.valid_actor_reference_in_private_actions.positive.with_entity.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.valid_actor_reference_in_private_actions.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.valid_actor_reference_in_private_actions"
            )
        )
        == 0
    )


def test_valid_actor_reference_in_private_actions_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_actor_reference_in_private_actions/"
    target_file_name = (
        f"reference_control.valid_actor_reference_in_private_actions.negative.xosc"
    )
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.valid_actor_reference_in_private_actions.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.valid_actor_reference_in_private_actions"
    )

    assert len(reference_issues) == 1
    assert reference_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_resolvable_entity_reference_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_entity_references/"
    target_file_name = f"reference_control.resolvable_entity_references.positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.resolvable_entity_references.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.resolvable_entity_references"
            )
        )
        == 0
    )


def test_resolvable_entity_reference_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_entity_references/"
    target_file_name = f"reference_control.resolvable_entity_references.negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.resolvable_entity_references.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.resolvable_entity_references"
    )
    assert len(reference_issues) == 1
    assert reference_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_resolvable_entity_reference_negative_multiple(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_entity_references/"
    target_file_name = (
        f"reference_control.resolvable_entity_references.negative.multiple.xosc"
    )
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.resolvable_entity_references.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.resolvable_entity_references"
    )
    assert len(reference_issues) == 2
    assert reference_issues[0].level == IssueSeverity.ERROR
    assert reference_issues[1].level == IssueSeverity.ERROR
    assert "Vehicle 3" in reference_issues[0].locations[0].description
    assert "Vehicle 4" in reference_issues[1].locations[0].description
    test_utils.cleanup_files()


def test_resolvable_variable_reference_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_variable_reference/"
    target_file_name = f"reference_control.resolvable_variable_reference.positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.resolvable_entity_references.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.resolvable_variable_reference"
            )
        )
        == 0
    )


def test_resolvable_variable_reference_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_variable_reference/"
    target_file_name = f"reference_control.resolvable_variable_reference.negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.resolvable_variable_reference.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.resolvable_variable_reference"
    )
    assert len(reference_issues) == 1
    assert reference_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_resolvable_variable_reference_multiple(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_variable_reference/"
    target_file_name = (
        f"reference_control.resolvable_variable_reference.negative.multiple.xosc"
    )
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.resolvable_variable_reference.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.resolvable_variable_reference"
    )
    assert len(reference_issues) == 2
    assert reference_issues[0].level == IssueSeverity.ERROR
    assert reference_issues[1].level == IssueSeverity.ERROR
    assert (
        "unknownReferenceForYPosition" in reference_issues[0].locations[0].description
    )
    assert "foo" in reference_issues[1].locations[0].description
    test_utils.cleanup_files()


def test_resolvable_storyboard_element_reference_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_storyboard_element_reference/"
    target_file_name = f"resolvable_storyboard_element_reference.positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.resolvable_storyboard_element_reference.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.resolvable_storyboard_element_reference"
            )
        )
        == 0
    )


def test_resolvable_storyboard_element_reference_positive_parameter(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_storyboard_element_reference/"
    target_file_name = (
        f"resolvable_storyboard_element_reference.positive.parameter.xosc"
    )
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.resolvable_storyboard_element_reference.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.resolvable_storyboard_element_reference"
            )
        )
        == 0
    )


def test_resolvable_storyboard_element_reference_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_storyboard_element_reference/"
    target_file_name = f"resolvable_storyboard_element_reference.negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.resolvable_storyboard_element_reference.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.resolvable_storyboard_element_reference"
    )
    assert len(reference_issues) == 2
    assert reference_issues[0].level == IssueSeverity.ERROR
    assert reference_issues[1].level == IssueSeverity.ERROR
    assert "Act2" in reference_issues[0].locations[0].description
    assert "Act1" in reference_issues[1].locations[0].description

    test_utils.cleanup_files()


def test_resolvable_storyboard_element_reference_negative_parameter(
    monkeypatch,
) -> None:
    base_path = "tests/data/resolvable_storyboard_element_reference/"
    target_file_name = (
        f"resolvable_storyboard_element_reference.negative.parameter.xosc"
    )
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.resolvable_storyboard_element_reference.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.resolvable_storyboard_element_reference"
    )
    assert len(reference_issues) == 1
    assert reference_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_unique_element_names_on_same_level_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/unique_element_names_on_same_level/"
    target_file_name = f"unique_element_names_on_same_level.positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.unique_element_names_on_same_level.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.unique_element_names_on_same_level"
            )
        )
        == 0
    )


def test_unique_element_names_on_same_level_positive_multiple(
    monkeypatch,
) -> None:
    base_path = "tests/data/unique_element_names_on_same_level/"
    target_file_name = f"unique_element_names_on_same_level.positive.multiple.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.unique_element_names_on_same_level.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:reference_control.unique_element_names_on_same_level"
            )
        )
        == 0
    )


def test_unique_element_names_on_same_level_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/unique_element_names_on_same_level/"
    target_file_name = f"unique_element_names_on_same_level.negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.unique_element_names_on_same_level.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.unique_element_names_on_same_level"
    )
    assert len(reference_issues) == 1
    assert reference_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_unique_element_names_on_same_level_negative_multiple(
    monkeypatch,
) -> None:
    base_path = "tests/data/unique_element_names_on_same_level/"
    target_file_name = f"unique_element_names_on_same_level.negative.multiple.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            reference_checker.unique_element_names_on_same_level.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    reference_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:reference_control.unique_element_names_on_same_level"
    )
    assert len(reference_issues) == 3
    assert reference_issues[0].level == IssueSeverity.ERROR
    assert reference_issues[1].level == IssueSeverity.ERROR
    assert reference_issues[2].level == IssueSeverity.ERROR

    assert "Story1" in reference_issues[0].locations[0].description
    assert "Event222" in reference_issues[1].locations[0].description
    assert "Event1" in reference_issues[2].locations[0].description
    test_utils.cleanup_files()
