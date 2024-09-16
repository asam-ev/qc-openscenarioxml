from dataclasses import dataclass
from lxml import etree
from typing import Union
from enum import Enum

from qc_baselib import Configuration, Result


@dataclass
class CheckerData:
    xml_file_path: str
    input_file_xml_root: Union[None, etree._ElementTree]
    config: Configuration
    result: Result
    schema_version: Union[None, str]
    xodr_root: Union[None, etree._ElementTree]


class AttributeType(Enum):
    VALUE = 0
    EXPRESSION = 1
    PARAMETER = 2
