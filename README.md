# asam-qc-openscenarioxml

This project implements the [ASAM OpenScenario XML Checker](checker_bundle_doc.md).

- [asam-qc-openscenarioxml](#asam-qc-openscenarioxml)
  - [Installation and usage](#installation-and-usage)
    - [Installation using pip](#installation-using-pip)
    - [Installation from source](#installation-from-source)
    - [Example output](#example-output)
  - [Register Checker Bundle to ASAM Quality Checker Framework](#register-checker-bundle-to-asam-quality-checker-framework)
    - [Linux Manifest Template](#linux-manifest-template)
  - [Tests](#tests)
  - [Contributing](#contributing)


## Installation and usage

asam-qc-openscenarioxml can be installed using pip or from source.

### Installation using pip

asam-qc-openscenarioxml can be installed using pip.

```bash
pip install asam-qc-openscenarioxml@git+https://github.com/asam-ev/qc-openscenarioxml@main
```

**Note**: To install from different sources, you can replace `@main` with
your desired target. For example, `develop` branch as `@develop`.

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

Manifest file templates are provided in the [manifest_templates](manifest_templates/) folder to register the ASAM OpenDrive Checker Bundle with the [ASAM Quality Checker Framework](https://github.com/asam-ev/qc-framework/tree/main).

### Linux Manifest Template

To register this Checker Bundle in Linux, use the [linux_manifest.json](manifest_templates/linux_manifest.json) template file. Replace the path to the Python executable `/home/user/.venv/bin/python` in the `exec_command` with the path to the Python executable where the Checker Bundle is installed.

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
