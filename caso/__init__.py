# -*- coding: utf-8 -*-

# Copyright 2014 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""cASO is an accounting extractor."""

import importlib.metadata
import pathlib
from contextlib import suppress

__version__ = "5.1.0"


def extract_version() -> str:
    """Return either the version of the package installed."""
    with suppress(FileNotFoundError, StopIteration):
        root_dir = pathlib.Path(__file__).parent.parent.parent
        with open(root_dir / "pyproject.toml", encoding="utf-8") as pyproject_toml:
            version = (
                next(line for line in pyproject_toml if line.startswith("version"))
                .split("=")[1]
                .strip("'\"\n ")
            )
            return f"{version}-dev (at {root_dir})"
    return importlib.metadata.version(__package__ or __name__.split(".", maxsplit=1)[0])


user_agent = f"caso/{__version__} (OpenStack)"
