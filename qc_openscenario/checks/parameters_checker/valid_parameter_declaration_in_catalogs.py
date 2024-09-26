import logging


from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_parameters_valid_parameter_declaration_in_catalogs"
CHECKER_DESCRIPTION = "All parameters used within a catalog shall be declared within their ParameterDeclaration in the same catalog, which sets a default value for each parameter."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.2.0:parameters.valid_parameter_declaration_in_catalogs"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xosc:1.2.0:parameters.valid_parameter_declaration_in_catalogs

    Description: All parameters used within a catalog shall be declared within their ParameterDeclaration in the same catalog,
                 which sets a default value for each parameter.
    Severity: ERROR

    Version range: [1.2.0, )

    Remark:
        None

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/16
    """
    logging.info("Executing valid_parameter_declaration_in_catalogs check")

    root = checker_data.input_file_xml_root

    catalogs_node = root.findall(".//Catalog")
    if catalogs_node is None:
        logging.error("Cannot find Catalog nodes in provided XOSC file. Skipping check")

        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            "Cannot find Catalog nodes in provided XOSC file. Skip the check.",
        )

        return

    logging.debug(f"catalogs_node : {catalogs_node}")

    for catalog_node in catalogs_node:

        parameter_declaration_nodes = catalog_node.find(".//ParameterDeclarations")
        logging.debug(f"parameter_declaration_nodes : {parameter_declaration_nodes}")
        # Get parameters declarations and check if they have default value
        defined_parameters_with_default = set()
        if parameter_declaration_nodes is not None:
            for declaration_node in list(parameter_declaration_nodes):
                current_name = declaration_node.get("name")
                current_default_value = declaration_node.get("value")

                if (
                    current_name is not None
                    and current_default_value is not None
                    and current_default_value != ""
                ):
                    defined_parameters_with_default.add(current_name)

        # Expression selecting when a node attribute value starts with $, indicating a parameter usage
        xpath_expr = './/*[@*[starts-with(., "$")]]'

        logging.debug(
            f"defined_parameters_with_default: {defined_parameters_with_default}"
        )
        nodes_with_parameters_attributes = catalog_node.xpath(xpath_expr)
        logging.debug(
            f"nodes_with_parameters_attributes: {nodes_with_parameters_attributes}"
        )

        for node_with_parameter_attribute in nodes_with_parameters_attributes:
            xpath = root.getpath(node_with_parameter_attribute)

            for attr_name, attr_value in node_with_parameter_attribute.attrib.items():
                if (
                    utils.get_attribute_type(attr_value)
                    == models.AttributeType.PARAMETER
                    and attr_value[1:] not in defined_parameters_with_default
                ):

                    issue_id = checker_data.result.register_issue(
                        checker_bundle_name=constants.BUNDLE_NAME,
                        checker_id=CHECKER_ID,
                        description="Parameter not defined or without default value within a catalog",
                        level=IssueSeverity.ERROR,
                        rule_uid=RULE_UID,
                    )
                    checker_data.result.add_xml_location(
                        checker_bundle_name=constants.BUNDLE_NAME,
                        checker_id=CHECKER_ID,
                        issue_id=issue_id,
                        xpath=xpath,
                        description=f"Parameter value {attr_value[1:]} for attribute {attr_name} is not defined in Catalog or has no default value",
                    )
