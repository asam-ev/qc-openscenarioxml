import logging


from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.reference_checker import reference_checker_precondition

CHECKER_ID = (
    "check_asam_xosc_reference_control_valid_actor_reference_in_private_actions"
)
MIN_RULE_VERSION = "1.2.0"


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

    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        description="In a ManeuverGroup, if the defined action is a private action an actor must be defined.",
    )

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting=MIN_RULE_VERSION,
        rule_full_name="reference_control.valid_actor_reference_in_private_actions",
    )

    if not checker_data.result.all_checkers_completed_without_issue(
        reference_checker_precondition.PRECONDITIONS
    ):
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        return

    schema_version = checker_data.schema_version
    if (
        schema_version is None
        or utils.compare_versions(schema_version, MIN_RULE_VERSION) < 0
    ):
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        return

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
                description="Issue flagging when no Actor is specified but a PrivateAction is used",
                level=IssueSeverity.ERROR,
                rule_uid=rule_uid,
            )
            private_actions_xpaths = [root.getpath(x) for x in private_actions]
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"ManeuverGroup at {xpath} uses private actions {private_actions_xpaths} but it defines no actor",
            )

    checker_data.result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        status=StatusType.COMPLETED,
    )
