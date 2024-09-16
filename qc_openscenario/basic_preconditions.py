from qc_openscenario.checks.basic_checker import (
    valid_xml_document,
    root_tag_is_openscenario,
    fileheader_is_present,
    version_is_defined,
)

from qc_openscenario.checks.schema_checker import valid_schema

CHECKER_PRECONDITIONS = {
    valid_xml_document.CHECKER_ID,
    root_tag_is_openscenario.CHECKER_ID,
    fileheader_is_present.CHECKER_ID,
    version_is_defined.CHECKER_ID,
    valid_schema.CHECKER_ID,
}
