from lxml import etree
from typing import Union
from qc_openscenario.checks import models
import re
import logging
import os

EXPRESSION_PATTERN = re.compile(r"[$][{][ A-Za-z0-9_\+\-\*/%$\(\)\.,]*[\}]")
PARAMETER_PATTERN = re.compile(r"[$][A-Za-z_][A-Za-z0-9_]*")


def get_standard_schema_version(root: etree._ElementTree) -> Union[str, None]:
    header = root.find("FileHeader")
    if header is None:
        return None
    header_attrib = header.attrib
    version = f"{header_attrib['revMajor']}.{header_attrib['revMinor']}.0"
    return version


def compare_versions(version1: str, version2: str) -> int:
    """Compare two version strings like "X.x.x"
        This function is to avoid comparing version string basing on lexicographical order
        that could cause problem. E.g.
        1.10.0 > 1.2.0 but lexicographical comparison of string would return the opposite

    Args:
        version1 (str): First string to compare
        version2 (str): Second string to compare

    Returns:
        int: 1 if version1 is bigger than version2. 0 if the version are the same. -1 otherwise
    """
    v1_components = list(map(int, version1.split(".")))
    v2_components = list(map(int, version2.split(".")))

    # Compare each component until one is greater or they are equal
    for v1, v2 in zip(v1_components, v2_components):
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1

    # If all components are equal, compare based on length
    if len(v1_components) < len(v2_components):
        return -1
    elif len(v1_components) > len(v2_components):
        return 1
    else:
        return 0


def get_parameter_value_from_node(
    tree: etree._ElementTree, node: etree._Element, parameter_name: str
) -> Union[None, str, int, float]:
    """Read all ParameterDeclaration visible from node and get the value of parameter_name if present

    Args:
        root (etree._ElementTree): root node of the xml document
        node (etree._Element): node to start the upward search from
        parameter_name (str): the parameter name to search

    Returns:
        Union[None, str, int, float]: the parameter value is present, with its type. None if the parameter_name is not found
    """
    # Dictionary to hold parameters
    params_dict = {}
    parameter_xpath = "./ParameterDeclarations/ParameterDeclaration"

    current = node
    while current is not None:
        for param in current.xpath(parameter_xpath):
            name = param.get("name")
            value = param.get("value")
            if name not in params_dict:
                params_dict[name] = value
        current = current.getparent()

    logging.debug(f"Visible parameters dictionary: {params_dict}")

    if parameter_name in params_dict:
        return params_dict[parameter_name]
    else:
        return None


def get_xodr_road_network(
    input_file_path: str, tree: etree._ElementTree
) -> Union[etree._ElementTree, None]:
    """Get parsed xodr tree indicated in the RoadNetwork/LogicFile node of the input tree

    Args:
        tree (etree._ElementTree): xml document tree that refers to a xodr file

    Returns:
        Union[etree._ElementTree, None]: the parsed road network tree.
                                         None if the specified nodes in the root or the road network file are not found
    """

    road_network = tree.find("RoadNetwork")
    if road_network is None:
        return None
    logic_file = road_network.find("LogicFile")
    if logic_file is None:
        return None
    filepath = logic_file.get("filepath")
    if filepath is None:
        return None

    # If filepath is specified using param, get all param declaration and update the filepath
    if get_attribute_type(filepath) == models.AttributeType.PARAMETER:
        filepath_param = filepath[1:]
        filepath = get_parameter_value_from_node(tree, tree.getroot(), filepath_param)
        if filepath is None:
            return None

    previous_wd = os.getcwd()
    os.chdir(os.path.dirname(input_file_path))

    xodr_root = etree.parse(filepath)

    os.chdir(previous_wd)

    return xodr_root


def get_attribute_type(attribute_value: str) -> models.AttributeType:
    """Given attribute value as input, checks if it is an expression, a parameter or a plain string

    Args:
        attribute_value (str): the attribute value to check

    Returns:
        models.AttributeType: enum representing whether attribute value is
            - expression (AttributeType.EXPRESSION),
            - parameter (AttributeType.PARAMETER)
            - a plain string (AttributeType.STRING)
    """

    if EXPRESSION_PATTERN.match(attribute_value):
        return models.AttributeType.EXPRESSION
    elif PARAMETER_PATTERN.match(attribute_value):
        return models.AttributeType.PARAMETER

    return models.AttributeType.VALUE


def is_xsd_double(input_str: str) -> bool:
    """Checks if input string follows xsd double specification
    The pattern is built following xsd double definition from http://www.datypic.com/sc/xsd/t-xsd_double.html

    Args:
        input_str (str): The input string to check

    Returns:
        bool: True if the input string represent a valid xsd:double value. False otherwise
    """
    pattern = re.compile(r"^([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?|INF|-INF|NaN)$")
    return pattern.match(input_str) is not None
