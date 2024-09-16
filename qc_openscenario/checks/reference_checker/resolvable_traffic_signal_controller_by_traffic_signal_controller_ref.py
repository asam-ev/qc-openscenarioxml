import logging

from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_reference_control_resolvable_traffic_signal_controller_by_traffic_signal_controller_ref"
CHECKER_DESCRIPTION = "The trafficSignalController according to the trafficSignalControllerRef property must exist within the scenarios RoadNetwork definition."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.2.0:reference_control.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xosc:1.2.0:reference_control.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref

    Description: The trafficSignalController according to the "trafficSignalControllerRef" property must exist within the scenarios RoadNetwork definition.
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/14
    """
    logging.info(
        "Executing resolvable_traffic_signal_controller_by_traffic_signal_controller_ref check"
    )

    root = checker_data.input_file_xml_root

    road_network = root.find("RoadNetwork")
    if road_network is None:
        logging.error(
            "Cannot find RoadNetwork node in provided XOSC file. Skipping check"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    # ts = traffic signal
    ts_controllers = road_network.findall(".//TrafficSignalController")
    if ts_controllers is None:
        logging.error(
            "Cannot find TrafficSignalController nodes in RoadNetwork of provided XOSC file. Skipping check"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    ts_controller_names = set()
    for ts_controller in ts_controllers:
        current_name = ts_controller.get("name")
        if current_name is not None:
            ts_controller_names.add(current_name)

    ts_controller_actions = root.findall(".//TrafficSignalControllerAction")

    for ts_controller in ts_controller_actions:
        current_name = ts_controller.get("trafficSignalControllerRef")
        if current_name is not None and current_name not in ts_controller_names:
            xpath = root.getpath(ts_controller)

            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="Issue flagging traffic signal controller reference not present in the declared RoadNetwork",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"trafficSignalControllerRef at {xpath} with id {current_name} not found in RoadNetwork node",
            )
