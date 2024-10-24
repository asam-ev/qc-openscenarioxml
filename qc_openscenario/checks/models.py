from dataclasses import dataclass
from lxml import etree
from typing import Optional
from enum import Enum

from qc_baselib import Configuration, Result


@dataclass
class CheckerData:
    xml_file_path: str
    input_file_xml_root: Optional[etree._ElementTree]
    config: Configuration
    result: Result
    schema_version: Optional[str]
    xodr_root: Optional[etree._ElementTree]


class AttributeType(Enum):
    VALUE = 0
    EXPRESSION = 1
    PARAMETER = 2
