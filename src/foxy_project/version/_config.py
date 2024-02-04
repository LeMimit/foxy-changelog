# SPDX-FileCopyrightText: 2010-2024 Ronny Pfannschmidt <opensource@ronnypfannschmidt.de>
# SPDX-FileCopyrightText: 2024-present Fabien Hermitte
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import re

from dataclasses import dataclass
from pathlib import Path
from re import Pattern
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import TypeAlias
from typing import Union

from foxy_project.config.pyproject_reading import PYPROJECT
from foxy_project.config.pyproject_reading import get_args_for_pyproject
from foxy_project.config.pyproject_reading import read_changelog_config


if TYPE_CHECKING:
    import os

    import setuptools_scm


VERSION_SCHEME: TypeAlias = Union[str, Callable[["setuptools_scm.version.ScmVersion"], str]]
SCMVERSION: TypeAlias = "setuptools_scm.version.ScmVersion"
PathT: TypeAlias = Union["os.PathLike[str]", str]

DEFAULT_VERSION_SCHEME = "pep440-conventional-commit-foxy"
DEFAULT_LOCAL_SCHEME = "node-and-date"

# default tag regex that tries to match PEP440 style versions with prefix consisting of dashed words
DEFAULT_TAG_REGEX = re.compile(r"^(?:[\w-]+-)?(?P<version>[vV]?\d+(?:\.\d+){0,2}[^\+]*)(?:\+.*)?$")


@dataclass
class Configuration:
    """Global configuration model"""

    version_scheme: VERSION_SCHEME = DEFAULT_VERSION_SCHEME
    local_scheme: VERSION_SCHEME = DEFAULT_LOCAL_SCHEME
    version_file: PathT | None = None
    version_file_template: str | None = None
    relative_to: PathT | None = None
    tag_regex: str | Pattern[str] = DEFAULT_TAG_REGEX
    parentdir_prefix_version: str | None = None
    fallback_version: str | None = None
    fallback_root: PathT = "."
    normalize: bool = True
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
            setion_name="version", path=Path(name), use_tool_name=use_tool_name, require_section=_require_section
        )
        args = get_args_for_pyproject(pyproject_data, dist_name, kwargs)
        relative_to = args.pop("relative_to", name)
        return cls.from_data(relative_to=relative_to, data=args)

    @classmethod
    def from_data(cls, relative_to: str, data: dict[str, Any]) -> Configuration:
        """
        Given configuration data create a config instance.
        """
        return cls(relative_to=relative_to, **data)

    def copy(self, new: dict[str, Any]) -> Configuration:
        """
        Returns a copy of the current configuration updated with the no None fields of the given configuration.
        """
        self_as_dict = self.__dict__.copy()
        other_as_dict = {key: value for key, value in new.items() if value is not None}
        self_as_dict.update((key, value) for key, value in other_as_dict.items())
        return Configuration(**self_as_dict)
