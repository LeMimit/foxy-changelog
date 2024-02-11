# SPDX-FileCopyrightText: 2016-2024 Michael Bryan <michaelfbryan@gmail.com> - Ken Mijime <kenaco666@gmail.com>
# SPDX-FileCopyrightText: 2024-present Fabien Hermitte
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import re

from abc import ABC
from abc import abstractmethod
from enum import Enum
from typing import Any
from typing import Callable

from foxy_project.changelog import default_issue_pattern


# Default aim for Semver tags.
# Original Semver source: https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
semver_nammed_regex = r"(?P<version>((?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*))(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)"  # noqa: E501
calendar_nammed_regex = r"(?P<version>((?P<major>\d{4})\.(?P<minor>\d{2})\.(?P<patch>[1-9]\d*))(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)"  # noqa: E501
# Regex which allow to not have a patch
relaxed_semver_regex = r"((?:(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:\.(?:0|[1-9]\d*))?(?:-(?:(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?:[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?))"  # noqa: E501


class ChangeType(Enum):
    BUILD = "build"
    CI = "ci"
    CHORE = "chore"
    DEPS = "deps"
    DOCS = "docs"
    FEAT = "feat"
    FIX = "fix"
    PERF = "perf"
    REFACTOR = "refactor"
    REVERT = "revert"
    STYLE = "style"
    TEST = "test"
    TOOLS = "tools"
    VERSION = "version"


class Note:
    def __init__(
        self,
        sha: str,
        change_type: ChangeType | str,
        description: str,
        scope: str = "",
        body: str = "",
        footer: str = "",
    ):
        self.sha = sha
        self.change_type = ChangeType(change_type) if change_type else change_type  # TODO Hmm..
        self.scope = scope
        self.description = description
        self.body = body
        self.footer = footer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Note):
            return NotImplemented
        return (
            self.sha == other.sha
            and self.change_type == other.change_type
            and self.description == other.description
            and self.body == other.body
            and self.footer == other.footer
        )


class DependencyUpdate:
    def __init__(
        self,
        name: str,
        previous_version: str,
        next_version: str,
    ):
        self.name = name
        self.previous_version = previous_version
        self.next_version = next_version

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DependencyUpdate):
            return NotImplemented
        return (
            self.name == other.name
            and self.previous_version == other.previous_version
            and self.next_version == other.next_version
        )


class Release(Note):
    def __init__(
        self,
        title: str,
        tag: str,
        date: str,
        sha: str,
        *args: Any,
        change_type: str = "chore",
        description: str = "",
        **kwargs: Any,
    ):
        super().__init__(sha, change_type, description, *args, **kwargs)
        self.title = title
        self.tag = tag
        self.date = date
        self._notes: list[Note] = []
        self._changes_indicators = {type_: False for type_ in ChangeType}
        self.diff_url: str | None = None
        self.previous_tag: str | None = None

    @property
    def builds(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.BUILD)

    @property
    def ci(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.CI)

    @property
    def chore(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.CHORE)

    @property
    def deps(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.DEPS)

    @property
    def deps_table(self) -> list[DependencyUpdate]:
        deps_notes = self._notes_with_type(ChangeType.DEPS)
        map_deps: dict[str, DependencyUpdate] = {}
        regex = re.compile(f"from {relaxed_semver_regex} to {relaxed_semver_regex}")
        for deps_note in deps_notes:
            match = regex.match(deps_note.description)
            if match:
                if deps_note.scope in map_deps:
                    map_deps[deps_note.scope].previous_version = match.group(1)
                else:
                    map_deps[deps_note.scope] = DependencyUpdate(
                        name=deps_note.scope, previous_version=match.group(1), next_version=match.group(2)
                    )

        return list(map_deps.values())

    @property
    def docs(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.DOCS)

    @property
    def features(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.FEAT)

    @property
    def fixes(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.FIX)

    @property
    def performance_improvements(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.PERF)

    @property
    def refactorings(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.REFACTOR)

    @property
    def reverts(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.REVERT)

    @property
    def style_changes(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.STYLE)

    @property
    def tests(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.TEST)

    @property
    def tools(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.TOOLS)

    @property
    def version(self) -> tuple[Note, ...]:
        return self._notes_with_type(ChangeType.VERSION)

    @property
    def has_builds(self) -> bool:
        return self._has(ChangeType.BUILD)

    @property
    def has_ci(self) -> bool:
        return self._has(ChangeType.CI)

    @property
    def has_chore(self) -> bool:
        return self._has(ChangeType.CHORE)

    @property
    def has_deps(self) -> bool:
        return self._has(ChangeType.DEPS)

    @property
    def has_docs(self) -> bool:
        return self._has(ChangeType.DOCS)

    @property
    def has_features(self) -> bool:
        return self._has(ChangeType.FEAT)

    @property
    def has_fixes(self) -> bool:
        return self._has(ChangeType.FIX)

    @property
    def has_performance_improvements(self) -> bool:
        return self._has(ChangeType.PERF)

    @property
    def has_refactorings(self) -> bool:
        return self._has(ChangeType.REFACTOR)

    @property
    def has_reverts(self) -> bool:
        return self._has(ChangeType.REVERT)

    @property
    def has_style_changes(self) -> bool:
        return self._has(ChangeType.STYLE)

    @property
    def has_tests(self) -> bool:
        return self._has(ChangeType.TEST)

    @property
    def has_tools(self) -> bool:
        return self._has(ChangeType.TOOLS)

    @property
    def has_version(self) -> bool:
        return self._has(ChangeType.VERSION)

    def add_note(self, note: Note) -> None:
        self._notes.append(note)
        self._changes_indicators[note.change_type] = True

    def set_compare_url(self, diff_url: str, previous_tag: str) -> None:
        self.previous_tag = previous_tag
        self.diff_url = diff_url.format(previous=previous_tag, current=self.tag)

    def _notes_with(self, predicate: Callable) -> tuple[Note, ...]:
        filtered_note = filter(predicate, self._notes)
        return tuple(sorted(filtered_note, key=lambda note: note.scope))

    def _notes_with_type(self, type_: ChangeType) -> tuple[Note, ...]:
        return self._notes_with(lambda x: x.change_type == type_)

    def _has(self, type_: ChangeType) -> bool:
        return self._changes_indicators[type_]


class Changelog:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        title: str = "Changelog",
        description: str = "",
        issue_pattern: str | None = None,
        issue_url: str | None = None,
        tag_prefix: str = "",
        tag_pattern: str | None = None,
    ):
        self.title = title
        self.description = description
        logging.debug(default_issue_pattern)
        self.issue_pattern = issue_pattern or default_issue_pattern
        logging.debug(self.issue_pattern)
        self.issue_url = issue_url or ""
        logging.debug(issue_url)
        logging.debug(self.issue_url)
        self.tag_prefix = tag_prefix
        self.tag_pattern = tag_pattern or semver_nammed_regex
        self._releases: list[Release] = []
        self._current_release: Release | None = None

    def add_release(self, *args, **kwargs):
        """Add new Release. Require same arguments as :class:`Release`"""
        release = Release(*args, **kwargs)
        self._releases.append(release)
        self._current_release = release

    def add_note(self, *args, **kwargs):
        """Add new Note to current release. Require same arguments as :class:`Note`"""
        try:
            note = Note(*args, **kwargs)
        except ValueError as err:
            # Ignore exceptions raised by unsupported commit type.
            locallogger = logging.getLogger("Changelog.add_note")
            locallogger.debug("Ignore exception raised by unsupported commit: %s", err)
            return

        if not self._current_release:
            raise ValueError("There is no release, note can be added to")
        self._current_release.add_note(note)

    @property
    def releases(self) -> tuple[Release, ...]:
        """Returns iterable of releases sorted by date (newer first)"""
        return tuple(sorted(self._releases, key=lambda r: r.date, reverse=True))


class RepositoryInterface(ABC):  # pylint: disable=too-few-public-methods
    @abstractmethod
    def generate_changelog(  # pylint: disable=too-many-arguments
        self,
        title: str,
        description: str,
        remote: str,
        issue_pattern: str | None,
        issue_url: str | None,
        diff_url: str | None,
        starting_commit: str,
        stopping_commit: str,
    ) -> Changelog:
        raise NotImplementedError


class PresenterInterface(ABC):  # pylint: disable=too-few-public-methods
    @abstractmethod
    def present(self, changelog: Changelog) -> str:
        raise NotImplementedError
