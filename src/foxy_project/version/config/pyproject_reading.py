# SPDX-FileCopyrightText: 2010-2024 Ronny Pfannschmidt <opensource@ronnypfannschmidt.de>
# SPDX-FileCopyrightText: 2024-present Fabien Hermitte
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging

from typing import TYPE_CHECKING
from typing import NamedTuple

from foxy_project.version.config.setuptools import read_dist_name_from_setup_cfg
from foxy_project.version.config.toml import TOML_RESULT
from foxy_project.version.config.toml import read_toml_content


if TYPE_CHECKING:
    from pathlib import Path


_ROOT = "root"


class PyProjectData(NamedTuple):
    path: Path
    tool_name: str | None
    project: TOML_RESULT
    section: TOML_RESULT

    @property
    def project_name(self) -> str | None:
        return self.project.get("name")

    @property
    def project_description(self) -> str | None:
        return self.project.get("description")


def read_changelog_config(
    tool_name: str,
    path: Path,
    *,
    use_tool_name: bool = True,
    require_section: bool = True,
) -> PyProjectData:
    defn = read_toml_content(path, None if require_section else {})
    try:
        section = defn.get("tool", {})[tool_name]["changelog"] if use_tool_name else defn.get("changelog", {})
    except LookupError as e:
        error = f"{path} does not contain a tool.{tool_name} section"
        if require_section:
            raise LookupError(error) from e
        # logging.warning("toml section missing %r", error)
        section = {}

    project = defn.get("project", {})
    return PyProjectData(path, tool_name, project, section)


def get_args_for_pyproject(
    pyproject: PyProjectData,
    dist_name: str | None,
    kwargs: TOML_RESULT,
) -> TOML_RESULT:
    """drops problematic details and figures the distribution name"""
    section = pyproject.section.copy()
    kwargs = kwargs.copy()
    if "relative_to" in section:
        relative = section.pop("relative_to")
        logging.warning(
            "%s : at [tool.%s]\n" "ignoring value relative_to=%s" " as its always relative to the config file",
            pyproject.path,
            pyproject.tool_name,
            relative,
        )
    if "dist_name" in section:
        if dist_name is None:
            dist_name = section.pop("dist_name")
        else:
            assert dist_name == section["dist_name"]  # noqa: S101
            section.pop("dist_name")
    if dist_name is None:
        # minimal pep 621 support for figuring the pretend keys
        dist_name = pyproject.project_name
    if dist_name is None:
        dist_name = read_dist_name_from_setup_cfg()
    if _ROOT in kwargs:
        if kwargs[_ROOT] is None:
            kwargs.pop(_ROOT, None)
        elif _ROOT in section:
            if section[_ROOT] != kwargs[_ROOT]:
                logging.warning(f"root {section[_ROOT]} is overridden by the cli arg {kwargs[_ROOT]}")  # noqa: G004
            section.pop(_ROOT, None)
    return {"dist_name": dist_name, **section, **kwargs}
