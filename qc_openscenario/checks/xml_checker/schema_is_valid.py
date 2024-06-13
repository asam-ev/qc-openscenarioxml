import os, logging

from dataclasses import dataclass
from typing import List

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.schema import schema_files
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.xml_checker import xml_constants


def is_valid_xml(xml_tree: etree._ElementTree, schema_file: str) -> bool:
    """Check if input xml tree  is valid against the input schema file (.xsd)

    Args:
        xml_file (etree._ElementTree): XML tree to test
        schema_file (str): XSD file path containing the schema for the validation

    Returns:
        bool: True if file pointed by xml_file is valid w.r.t. input schema file. False otherwise
    """
    with open(schema_file, "rb") as schema_f:
        schema_doc = etree.parse(schema_f)
        schema = etree.XMLSchema(schema_doc)

    if schema.validate(xml_tree):
        logging.info("- XML is valid.")
        return True, None
    else:
        logging.error("- XML is invalid!")
        for error in schema.error_log:
            logging.error(f"- Error: {error.message}")
            logging.error(f"- Line: {error.line}, Column: {error.column}")

        return False, schema.error_log


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if input file is a valid xml document
    """
    logging.info("Executing schema_is_valid check")

    schema_version = checker_data.schema_version
    if schema_version is None:
        logging.info(f"- Version not found in the file. Skipping check")
        return

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=xml_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting=schema_version,
        rule_full_name="xml.schema_is_valid",
    )

    schema_files_dict = schema_files.SCHEMA_FILES

    if schema_version not in schema_files_dict:
        logging.info(f"- Version {schema_version} unsupported. Skipping check")
        return

    xsd_file = schema_files_dict[schema_version]
    xsd_file_path = os.path.join("qc_openscenario", "schema", xsd_file)

    is_valid, errors = is_valid_xml(checker_data.input_file_xml_root, xsd_file_path)

    if not is_valid:

        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=xml_constants.CHECKER_ID,
            description="Issue flagging when input file does not follow its version schema",
            level=IssueSeverity.ERROR,
            rule_uid=rule_uid,
        )

        for error in errors:
            checker_data.result.add_file_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=xml_constants.CHECKER_ID,
                issue_id=issue_id,
                row=error.line,
                column=error.column,
                file_type="xosc",
                description=error.message,
            )
