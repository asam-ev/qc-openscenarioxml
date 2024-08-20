# asam-qc-openscenarioxml

This project implements the [ASAM OpenScenario XML Checker](checker_bundle_doc.md).

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

After cloning the repository, there are two options to install from source.

1. Default Python on the machine
2. [Poetry](https://python-poetry.org/)

#### Default Python

```bash
pip install -r requirements.txt
```

This will install the needed dependencies to your local Python.

#### Poetry

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

## Tests

To run the tests, you need to install the extra test dependency after installing from source.

### Install using pip

```bash
pip install -r requirements-tests.txt
```

### Install using poetry

```bash
poetry install --with dev
```

### Execute tests


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
pip install -r requirements-dev.txt
```

or

```bash
poetry install --with dev
```

You need to have pre-commit installed and install the hooks:

```
pre-commit install
```
