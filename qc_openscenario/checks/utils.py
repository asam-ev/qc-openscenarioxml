from lxml import etree
from typing import Union


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


def get_parameter_value(
    root: etree._ElementTree, parameter_name: str
) -> Union[None, str, int, float]:
    """Read all ParameterDeclaration nodes from root and get the value of parameter_name if present

    Args:
        root (etree._ElementTree): root node of the xml document
        parameter_name (str): the parameter name to search

    Returns:
        Union[None, str, int, float]: the parameter value is present, with its type. None if the parameter_name is not found
    """
    param_declarations = root.findall(".//ParameterDeclaration")
    if param_declarations is None:
        return None

    for param_declaration in param_declarations:
        current_name = param_declaration.get("name")
        current_value = param_declaration.get("value")
        if (
            current_name is not None
            and current_value is not None
            and current_name == parameter_name
        ):
            return current_value

    return None


def get_xodr_road_network(root: etree._ElementTree) -> Union[etree._ElementTree, None]:
    """Get parsed xodr tree indicated in the RoadNetwork/LogicFile node of the input root

    Args:
        root (etree._ElementTree): root node of the xml document that refers to a xodr file

    Returns:
        Union[etree._ElementTree, None]: the parsed road network tree.
                                         None if the specified nodes in the root or the road network file are not found
    """
    road_network = root.find("RoadNetwork")
    if road_network is None:
        return None
    logic_file = road_network.find("LogicFile")
    if logic_file is None:
        return None
    filepath = logic_file.get("filepath")
    if filepath is None:
        return None

    # If filepath is specified using param, get all param declaration and update the filepath
    if filepath.startswith("$"):

        filepath_param = filepath[1:]
        filepath = get_parameter_value(root, filepath_param)
        if filepath is None:
            return None

    return etree.parse(filepath)
