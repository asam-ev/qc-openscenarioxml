import logging


from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models
from qc_openscenario.checks.reference_checker import reference_checker_precondition

CHECKER_ID = "check_asam_xosc_reference_control_resolvable_variable_reference"
MIN_RULE_VERSION = "1.2.0"
RULE_SEVERITY = IssueSeverity.ERROR


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xosc:1.2.0:reference_control.resolvable_variable_reference

    Description: The VariableDeclaration according to the "variableRef" property must exist within the ScenarioDefinition.
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/18
    """
    logging.info("Executing resolvable_variable_reference check")

    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        description="The VariableDeclaration according to the variableRef property must exist within the ScenarioDefinition.",
    )

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting=MIN_RULE_VERSION,
        rule_full_name="reference_control.resolvable_variable_reference",
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

    parameter_declaration_nodes = root.find("ParameterDeclarations")
    variable_declaration_nodes = root.find("VariableDeclarations")

    # Get parameters and variables declarations
    defined_param_variables = set()
    if parameter_declaration_nodes is not None:
        for declaration_node in list(parameter_declaration_nodes):
            current_name = declaration_node.get("name")
            if current_name is not None:
                defined_param_variables.add(current_name)

    if variable_declaration_nodes is not None:
        for declaration_node in list(variable_declaration_nodes):
            current_name = declaration_node.get("name")
            if current_name is not None:
                defined_param_variables.add(current_name)

    storyboard_node = root.find("Storyboard")
    if storyboard_node is None:
        logging.error(
            "Cannot find Storyboard node in provided XOSC file. Skipping check"
        )

        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        return

    nodes_with_variable_ref = storyboard_node.xpath(".//*[@variableRef]")

    for node_with_variable_ref in nodes_with_variable_ref:
        current_name = node_with_variable_ref.get("variableRef")
        if current_name is not None and current_name not in defined_param_variables:
            xpath = root.getpath(node_with_variable_ref)

            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="Issue flagging when a variable is referred in a variableRef attribute but it is not found within ScenarioDefinition",
                level=RULE_SEVERITY,
                rule_uid=rule_uid,
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=xpath,
                description=f"Variable with id {current_name} not found within ScenarioDefinition",
            )

    checker_data.result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        status=StatusType.COMPLETED,
    )
