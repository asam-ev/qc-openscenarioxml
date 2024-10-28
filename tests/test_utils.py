# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import sys
import pytest
from typing import List
import qc_openscenario.main as main
from qc_openscenario import constants, checks
from qc_baselib import Configuration, Result


CONFIG_FILE_PATH = "bundle_config.xml"
REPORT_FILE_PATH = "xosc_bundle_report.xqar"


def create_test_config(target_file_path: str):
    test_config = Configuration()
    test_config.set_config_param(name="InputFile", value=target_file_path)
    test_config.register_checker_bundle(checker_bundle_name=constants.BUNDLE_NAME)
    test_config.set_checker_bundle_param(
        checker_bundle_name=constants.BUNDLE_NAME,
        name="resultFile",
        value=REPORT_FILE_PATH,
    )

    test_config.write_to_file(CONFIG_FILE_PATH)


def launch_main(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["main.py", "-c", CONFIG_FILE_PATH, "--generate_markdown"],
    )
    main.main()


def cleanup_files():
    os.remove(REPORT_FILE_PATH)
    os.remove(CONFIG_FILE_PATH)
