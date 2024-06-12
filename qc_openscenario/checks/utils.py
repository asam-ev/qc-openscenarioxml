from lxml import etree


def get_standard_schema_version(root: etree._ElementTree) -> str:
    header = root.find("FileHeader")
    header_attrib = header.attrib
    version = f"{header_attrib['revMajor']}.{header_attrib['revMinor']}.0"
    return version
