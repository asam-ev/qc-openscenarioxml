# qc-openscenarioxml

This project implements the OpenScenario Checker for the ASAM Quality Checker project.

## Installation

To install the project, run:

```
pip install -r requirements.txt
```

This will install the needed dependencies to your local Python.

## Usage

The checker can be used as a Python script:

```
python main.py --help
usage: QC OpenScenario Checker [-h] (-d | -c CONFIG_PATH)
This is a collection of scripts for checking validity of OpenScenario (.xosc) files.
options:
  -h, --help            show this help message and exit
  -d, --default_config
  -c CONFIG_PATH, --config_path CONFIG_PATH
```

### Example

- No issues found

```
python3 main.py -c example_config.xml
2024-06-12 15:14:11,864 - Initializing checks
2024-06-12 15:14:11,865 - Executing xml checks
2024-06-12 15:14:11,865 - Executing is_an_xml_document check
asam.net:xosc:0.9.0:is_an_xml_document
2024-06-12 15:14:11,865 - Issues found - 0
2024-06-12 15:14:11,865 - Done
```


- Issues found on file

```
python3 main.py -c example_config.xml
2024-06-12 15:19:45,139 - Initializing checks
2024-06-12 15:19:45,140 - Executing xml checks
2024-06-12 15:19:45,140 - Executing is_an_xml_document check
asam.net:xosc:0.9.0:is_an_xml_document
2024-06-12 15:19:45,140 - Issues found - 1
2024-06-12 15:19:45,141 - Done

```


## Tests

To run the tests, you need to have installed the main dependencies mentioned
at [Installation](#installation).

Install Python tests and development dependencies:

```
pip install -r requirements-tests.txt
```

Execute tests:

```
python -m pytest -vv
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

```
pip install -r requirements-dev.txt
```

You need to have pre-commit installed and install the hooks:

```
pre-commit install
```
