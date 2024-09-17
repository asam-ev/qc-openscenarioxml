import logging


from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import models

from qc_openscenario import basic_preconditions

CHECKER_ID = (
    "check_asam_xosc_reference_control_valid_actor_reference_in_private_actions"
)
CHECKER_DESCRIPTION = "In a ManeuverGroup, if the defined action is a private action an actor must be defined."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = (
    "asam.net:xosc:1.2.0:reference_control.valid_actor_reference_in_private_actions"
)


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xosc:1.2.0:reference_control.valid_actor_reference_in_private_actions

    Description: In a ManeuverGroup, if the defined action is a private action an actor must be defined.

    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/17
    """
    logging.info("Executing valid_actor_reference_in_private_actions check")

    root = checker_data.input_file_xml_root

    maneuver_groups = root.findall(".//ManeuverGroup")
    if maneuver_groups is None:
        logging.error(
            "Cannot find ManeuverGroup node in provided XOSC file. Skipping check"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    for maneuver_group in maneuver_groups:

        private_actions = maneuver_group.findall(".//PrivateAction")
        entity_refs = maneuver_group.findall(".//EntityRef")

        if private_actions is None or entity_refs is None:
            logging.error(
                "Cannot find PrivateAction or EntityRef node in provided XOSC file. Skipping check"
            )

            checker_data.result.set_checker_status(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                status=StatusType.SKIPPED,
            )
            return

        has_private_action = len(private_actions) > 0
        no_actor_provided = len(entity_refs) == 0

        has_issue = has_private_action and no_actor_provided

        if has_issue:
            xpath = root.getpath(maneuver_group)
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="No Actor is specified but a PrivateAction is used",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )
            private_actions_xpaths = [root.getpath(x) for x in private_actions]
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"ManeuverGroup at {xpath} uses private actions {private_actions_xpaths} but it defines no actor",
            )
