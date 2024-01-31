# SPDX-FileCopyrightText: 2010-2024 Ronny Pfannschmidt <opensource@ronnypfannschmidt.de>
# SPDX-FileCopyrightText: 2024-present Fabien Hermitte
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from foxy_project.changelog.domain_model import calendar_nammed_regex
from foxy_project.changelog.domain_model import semver_nammed_regex
from foxy_project.changelog.repository import GitRepository


if TYPE_CHECKING:
    from typing import Callable
    from typing import Concatenate
    from typing import ParamSpec

    from setuptools_scm.version import ScmVersion

    _P = ParamSpec("_P")


VERSION_LEN = 3
VERSION_MINOR = 2
VERSION_PATCH = 3
CALENDAR_DECEMBER_MONTH = 12


def calendar_conventional_commit_foxy(version: ScmVersion) -> str:
    return _conventional_commit_foxy(version, tag_pattern=calendar_nammed_regex, guess_next=guess_next_simple_calendar)


def semver_conventional_commit_foxy(version: ScmVersion) -> str:
    return _conventional_commit_foxy(version, tag_pattern=semver_nammed_regex, guess_next=guess_next_simple_semver)


def _conventional_commit_foxy(
    version: ScmVersion, tag_pattern: str, guess_next: Callable[Concatenate[ScmVersion, _P], str]
) -> str:
    if version.exact:
        return version.format_with("{tag}")

    repository = GitRepository(
        Path("."),
        latest_version=None,
        skip_unreleased=False,
        tag_prefix="",
        tag_pattern=tag_pattern,
    )
    changelog = repository.generate_changelog()

    if changelog.releases[0].has_features:
        return version.format_next_version(guess_next, retain=VERSION_MINOR)

    return version.format_next_version(guess_next, retain=VERSION_PATCH)


def guess_next_simple_calendar(version: ScmVersion, *, retain: int, increment: bool = True) -> str:
    try:
        parts = [int(i) for i in str(version.tag).split(".")[:retain]]
    except ValueError:
        msg: str = f"{version} can't be parsed as numeric version"
        raise ValueError(msg) from None
    while len(parts) < retain:
        parts.append(1)
    if increment:
        parts[-1] += 1
    # Increment the major et reset month to 1 at the end of the year
    if parts[-1] > CALENDAR_DECEMBER_MONTH and retain == VERSION_MINOR:
        parts[-2] += 1
        parts[-1] = 1
    while len(parts) < VERSION_LEN:
        parts.append(1)
    return f"{parts[0]:04}.{parts[1]:02}.{parts[2]:01}"


def guess_next_simple_semver(version: ScmVersion, *, retain: int, increment: bool = True) -> str:
    try:
        parts = [int(i) for i in str(version.tag).split(".")[:retain]]
    except ValueError:
        msg: str = f"{version} can't be parsed as numeric version"
        raise ValueError(msg) from None
    while len(parts) < retain:
        parts.append(0)
    if increment:
        parts[-1] += 1
    while len(parts) < VERSION_LEN:
        parts.append(0)
    return ".".join(str(i) for i in parts)
