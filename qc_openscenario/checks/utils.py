from lxml import etree
from typing import Union


def get_standard_schema_version(root: etree._ElementTree) -> Union[str, None]:
    header = root.find("FileHeader")
    if header is None:
        return None
    header_attrib = header.attrib
    version = f"{header_attrib['revMajor']}.{header_attrib['revMinor']}.0"
    return version
