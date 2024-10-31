# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
