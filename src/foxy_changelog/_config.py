from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from foxy_changelog.setuptools_scm.code.pyproject_reading import get_args_for_pyproject
from foxy_changelog.setuptools_scm.code.pyproject_reading import read_pyproject


@dataclass
class Configuration:
    """Global configuration model"""

    gitlab: bool = False
    github: bool = True
    title: str | None = None
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
        name: str = "pyproject.toml",
        dist_name: str | None = None,
        *,
        _require_section: bool = False,
        **kwargs: Any,
    ) -> Configuration:
        """
        Read Configuration from pyproject.toml (or similar).
        Raises exceptions when file is not found or toml is not installed or the file has invalid format or does
        not contain the [tool.foxy_changelog] section.
        """
        pyproject_data = read_pyproject(tool_name="foxy-changelog", path=Path(name), require_section=_require_section)
        args = get_args_for_pyproject(pyproject_data, dist_name, kwargs)
        if "pyproject.toml" in name:
            args["title"] = pyproject_data.project_name
            args["description"] = pyproject_data.project_description

        # args.update(read_toml_overrides(args["dist_name"]))
        # relative_to = args.pop("relative_to", name)
        return cls.from_data(data=args)

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Configuration:
        """
        given configuration data create a config instance after validating tag regex/version class
        """
        # tag_regex = _check_tag_regex(data.pop("tag_regex", None))
        # version_cls = _validate_version_cls(data.pop("version_cls", None), data.pop("normalize", True))
        return cls(**data)

    def copy(self, new: dict[str, Any]) -> Configuration:
        """
        Returns a copy of the current configuration updated with the not None fields of the given configuration.
        """
        self_as_dict = self.__dict__.copy()
        other_as_dict = {key: value for key, value in new.items() if value is not None}
        self_as_dict.update((key, value) for key, value in other_as_dict.items())
        return Configuration(**self_as_dict)
