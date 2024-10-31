# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models
from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_reference_control_resolvable_signal_id_in_traffic_signal_state_action"
CHECKER_DESCRIPTION = "TrafficSignalStateAction:name -> Signal ID must exist within the given road network."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.2.0:reference_control.resolvable_signal_id_in_traffic_signal_state_action"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xosc:1.2.0:reference_control.resolvable_signal_id_in_traffic_signal_state_action

    Description: TrafficSignalStateAction:name -> Signal ID must exist within the given road network
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/13
    """
    logging.info("Executing resolvable_signal_id_in_traffic_signal_state_action check")

    root = checker_data.input_file_xml_root

    if checker_data.xodr_root is None:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            "Cannot read xodr file. Skip the check.",
        )

        return

    xodr_signal_list = checker_data.xodr_root.findall(".//signal")

    if xodr_signal_list is None:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            "Cannot read signals from xodr file. Skip the check.",
        )

        return

    xodr_signal_ids = set()
    for xodr_signal in xodr_signal_list:
        signal_id = xodr_signal.get("id")
        if signal_id is not None:
            xodr_signal_ids.add(signal_id)

    xosc_traffic_lights = root.findall(".//TrafficSignalStateAction")

    for xosc_traffic_light in xosc_traffic_lights:
        current_name = xosc_traffic_light.get("name")

        if current_name is not None and current_name not in xodr_signal_ids:
            xpath = root.getpath(xosc_traffic_light)
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="Traffic light id not present in linked xodr file",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"Traffic Light {xpath} with id {current_name} not found in xodr file",
            )
