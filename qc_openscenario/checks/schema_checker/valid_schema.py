# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import importlib.resources
import logging

from lxml import etree

from qc_baselib import IssueSeverity, StatusType

from qc_openscenario import constants
from qc_openscenario.schema import schema_files
from qc_openscenario.checks import models

from qc_openscenario.checks.basic_checker import (
    valid_xml_document,
    root_tag_is_openscenario,
    fileheader_is_present,
    version_is_defined,
)

CHECKER_ID = "check_asam_xosc_xml_valid_schema"
CHECKER_DESCRIPTION = "Input xml file must be valid according to the schema."
CHECKER_PRECONDITIONS = {
    valid_xml_document.CHECKER_ID,
    root_tag_is_openscenario.CHECKER_ID,
    fileheader_is_present.CHECKER_ID,
    version_is_defined.CHECKER_ID,
}
RULE_UID = "asam.net:xosc:1.0.0:xml.valid_schema"


def _is_schema_compliant(
    xml_tree: etree._ElementTree, schema_file: str
) -> tuple[bool, etree._ListErrorLog]:
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
    Implements a rule to check if input file is valid according to OpenSCENARIO schema

    More info at
        - https://github.com/asam-ev/qc-openscenarioxml/issues/2
    """
    logging.info("Executing valid_schema check")

    schema_version = checker_data.schema_version
    xsd_file = schema_files.SCHEMA_FILES.get(schema_version)

    if xsd_file is None:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            f"- Schema file for version {schema_version} does not exist. Skip the check.",
        )

        return

    xsd_file_path = str(
        importlib.resources.files("qc_openscenario.schema").joinpath(xsd_file)
    )
    schema_compliant, errors = _is_schema_compliant(
        checker_data.input_file_xml_root, xsd_file_path
    )

    if not schema_compliant:
        for error in errors:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="Input file does not follow its version schema",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )
            checker_data.result.add_file_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                row=error.line,
                column=error.column,
                description=error.message,
            )
