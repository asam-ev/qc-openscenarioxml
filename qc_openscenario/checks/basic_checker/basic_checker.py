import logging
import os

from lxml import etree

from qc_baselib import Configuration, Result, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.basic_checker import (
    valid_xml_document,
    root_tag_is_openscenario,
    fileheader_is_present,
    version_is_defined,
)


def run_checks(config: Configuration, result: Result) -> models.CheckerData:
    logging.info("Executing basic checks")

    xml_file_path = config.get_config_param("InputFile")

    valid_xml_document.check_rule(xml_file_path, result)

    root = None
    if result.all_checkers_completed_without_issue({valid_xml_document.CHECKER_ID}):
        root = utils.get_root_without_default_namespace(xml_file_path)

    root_tag_is_openscenario.check_rule(root, result)
    fileheader_is_present.check_rule(root, result)
    version_is_defined.check_rule(root, result)

    checker_data = None

    if result.all_checkers_completed_without_issue(
        {
            valid_xml_document.CHECKER_ID,
            root_tag_is_openscenario.CHECKER_ID,
            fileheader_is_present.CHECKER_ID,
            version_is_defined.CHECKER_ID,
        }
    ):
        xosc_schema_version = utils.get_standard_schema_version(root)
        xodr_root = utils.get_xodr_road_network(xml_file_path, root)
        checker_data = models.CheckerData(
            input_file_xml_root=root,
            config=config,
            result=result,
            schema_version=xosc_schema_version,
            xodr_root=xodr_root,
        )
    else:
        logging.info("Error found in basic rules!")
        checker_data = models.CheckerData(
            input_file_xml_root=None,
            config=config,
            result=result,
            schema_version=None,
            xodr_root=None,
        )

    return checker_data
