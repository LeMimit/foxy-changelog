# SPDX-FileCopyrightText: 2016-2024 Michael Bryan <michaelfbryan@gmail.com> - Ken Mijime <kenaco666@gmail.com>
# SPDX-FileCopyrightText: 2024-present Fabien Hermitte
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from foxy_project.version.config.pyproject_reading import get_args_for_pyproject
from foxy_project.version.config.pyproject_reading import read_changelog_config


PYPROJECT = "pyproject.toml"
FOXY_PROJECT_TOML = "foxy-project.toml"


@dataclass
class Configuration:
    """Global configuration model"""

    gitlab: bool = False
    github: bool = True
    title: str | None = "Changelog"
    description: str | None = None
    output: Path = Path("CHANGELOG.md")
    remote: str = "origin"
    latest_version: str | None = None
    unreleased: bool = False
    template: str = "compact"
    diff_url: str | None = None
    issue_url: str | None = None
    issue_pattern: str = r"(#([\w-]+))"
    tag_pattern: str = "semver"
    tag_prefix: str = ""
    stdout: bool = False
    starting_commit: str = ""
    stopping_commit: str = "HEAD"
    dist_name: str | None = None
    root: str = "."

    @classmethod
    def from_file(
        cls,
        name: str,
        dist_name: str | None = None,
        *,
        _require_section: bool = False,
        **kwargs: Any,
    ) -> Configuration:
        """
        Read Configuration from file.
        Raises exceptions when file is not found or toml is not installed or the file has invalid format.
        """

        use_tool_name = PYPROJECT in name
        pyproject_data = read_changelog_config(
            tool_name="foxy-project", path=Path(name), use_tool_name=use_tool_name, require_section=_require_section
        )
        args = get_args_for_pyproject(pyproject_data, dist_name, kwargs)
        # Take configuration from project as default configuration
        if PYPROJECT in name:
            if "title" not in args:
                args["title"] = pyproject_data.project_name
            if "description" not in args:
                args["description"] = pyproject_data.project_description
        return cls.from_data(data=args)

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Configuration:
        """
        Given configuration data create a config instance.
        """
        return cls(**data)

    def copy(self, new: dict[str, Any]) -> Configuration:
        """
        Returns a copy of the current configuration updated with the no None fields of the given configuration.
        """
        self_as_dict = self.__dict__.copy()
        other_as_dict = {key: value for key, value in new.items() if value is not None}
        self_as_dict.update((key, value) for key, value in other_as_dict.items())
        return Configuration(**self_as_dict)
