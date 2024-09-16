# asam-qc-openscenarioxml

This project implements the [ASAM OpenScenario XML Checker Bundle](checker_bundle_doc.md).

- [asam-qc-openscenarioxml](#asam-qc-openscenarioxml)
  - [Installation and usage](#installation-and-usage)
    - [Installation using pip](#installation-using-pip)
    - [Installation from source](#installation-from-source)
    - [Example output](#example-output)
  - [Register Checker Bundle to ASAM Quality Checker Framework](#register-checker-bundle-to-asam-quality-checker-framework)
    - [Linux Manifest Template](#linux-manifest-template)
    - [Windows Manifest Template](#windows-manifest-template)
    - [Example Configuration File](#example-configuration-file)
  - [Tests](#tests)
  - [Contributing](#contributing)


## Installation and usage

asam-qc-openscenarioxml can be installed using pip or from source.

### Installation using pip

asam-qc-openscenarioxml can be installed using pip.

```bash
pip install asam-qc-openscenarioxml@git+https://github.com/asam-ev/qc-openscenarioxml@main
```

**Note:** The above command will install `asam-qc-openscenarioxml` from the `main` branch. If you want to install `asam-qc-openscenarioxml` from another branch or tag, replace `@main` with the desired branch or tag. It is also possible to install from a local directory.

```bash
pip install /home/user/qc-openscenarioxml
```

To run the application:

```bash
qc_openscenario --help
usage: QC OpenScenario Checker [-h] (-d | -c CONFIG_PATH)
This is a collection of scripts for checking validity of OpenScenario (.xosc) files.
options:
  -h, --help            show this help message and exit
  -d, --default_config
  -c CONFIG_PATH, --config_path CONFIG_PATH
```

The following commands are equivalent:

```bash
qc_openscenario --help
python qc_openscenario/main.py --help
python -m qc_openscenario.main --help
```

### Installation from source

After cloning the repository, install the project using [Poetry](https://python-poetry.org/).

```bash
poetry install
```

After installing from source, the usage are similar to above.

```bash
qc_openscenario --help
python qc_openscenario/main.py --help
python -m qc_openscenario.main --help
```

### Example output

- No issues found

```bash
python qc_openscenario/main.py -c example_config.xml

2024-06-12 15:14:11,864 - Initializing checks
2024-06-12 15:14:11,865 - Executing xml checks
2024-06-12 15:14:11,865 - Executing is_an_xml_document check
asam.net:xosc:0.9.0:is_an_xml_document
2024-06-12 15:14:11,865 - Issues found - 0
2024-06-12 15:14:11,865 - Done
```

- Issues found on file

```bash
python qc_openscenario/main.py -c example_config.xml

2024-06-12 15:19:45,139 - Initializing checks
2024-06-12 15:19:45,140 - Executing xml checks
2024-06-12 15:19:45,140 - Executing is_an_xml_document check
asam.net:xosc:0.9.0:is_an_xml_document
2024-06-12 15:19:45,140 - Issues found - 1
2024-06-12 15:19:45,141 - Done

```

## Register Checker Bundle to ASAM Quality Checker Framework

Manifest file templates are provided in the [manifest_templates](manifest_templates/) folder to register the ASAM OpenScenario XML Checker Bundle with the [ASAM Quality Checker Framework](https://github.com/asam-ev/qc-framework/tree/main).

### Linux Manifest Template

To register this Checker Bundle in Linux, use the [linux_xosc_manifest.json](manifest_templates/linux_xosc_manifest.json) template file.

If the asam-qc-openscenarioxml is installed in a virtual environment, the `exec_command` needs to be adjusted as follows:

```json
"exec_command": "source <venv>/bin/activate && cd $ASAM_QC_FRAMEWORK_WORKING_DIR && qc_openscenario -c $ASAM_QC_FRAMEWORK_CONFIG_FILE"
```

Replace `<venv>/bin/activate` by the path to your virtual environment.

### Windows Manifest Template

To register this Checker Bundle in Windows, use the [windows_xosc_manifest.json](manifest_templates/windows_xosc_manifest.json) template file.

If the asam-qc-openscenarioxml is installed in a virtual environment, the `exec_command` needs to be adjusted as follows:

```json
"exec_command": "C:\\> <venv>\\Scripts\\activate.bat && cd %ASAM_QC_FRAMEWORK_WORKING_DIR% && qc_openscenario -c %ASAM_QC_FRAMEWORK_CONFIG_FILE%"
```

Replace `C:\\> <venv>\\Scripts\\activate.bat` by the path to your virtual environment.

### Example Configuration File

An example configuration file for using this Checker Bundle within the ASAM Quality Checker Framework is as follows.

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Config>

    <Param name="InputFile" value="my_openscenarioxml_file.xosc" />

    <CheckerBundle application="xoscBundle">
        <Param name="resultFile" value="xosc_bundle_report.xqar" />
        <Checker checkerId="check_asam_xosc_xml_valid_xml_document" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_xml_root_tag_is_openscenario" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_xml_fileheader_is_present" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_xml_version_is_defined" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_xml_valid_schema" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_reference_control_uniquely_resolvable_entity_references" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_reference_control_resolvable_signal_id_in_traffic_signal_state_action" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_reference_control_resolvable_traffic_signal_controller_by_traffic_signal_controller_ref" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_reference_control_valid_actor_reference_in_private_actions" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_reference_control_resolvable_entity_references" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_reference_control_resolvable_variable_reference" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_reference_control_resolvable_storyboard_element_reference" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_reference_control_unique_element_names_on_same_level" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_parameters_valid_parameter_declaration_in_catalogs" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_data_type_allowed_operators" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_data_type_non_negative_transition_time_in_light_state_action" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_xosc_positive_duration_in_phase" maxLevel="1" minLevel="3" />
    </CheckerBundle>

    <ReportModule application="TextReport">
        <Param name="strInputFile" value="Result.xqar" />
        <Param name="strReportFile" value="Report.txt" />
    </ReportModule>

</Config>
```

## Tests

To run the tests, you need to install the extra test dependency after installing from source.

```bash
poetry install --with dev
```

To execute tests

```bash
python -m pytest -vv
```

or

```bash
poetry run pytest -vv
```

They should output something similar to:

```
===================== test session starts =====================
platform linux -- Python 3.11.9, pytest-8.2.2, pluggy-1.5.0
```

You can check more options for pytest at its [own documentation](https://docs.pytest.org/).

## Contributing

For contributing, you need to install the development requirements besides the
test and installation requirements, for that run:

```bash
poetry install --with dev
```

You need to have pre-commit installed and install the hooks:

```
pre-commit install
```
