# SPDX-FileCopyrightText: 2016-2024 Michael Bryan <michaelfbryan@gmail.com> - Ken Mijime <kenaco666@gmail.com>
# SPDX-FileCopyrightText: 2024-present Fabien Hermitte
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import re

from datetime import date
from enum import StrEnum
from hashlib import sha256
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional

from git import Repo
from git import TagReference

from foxy_project.changelog import default_diff_url
from foxy_project.changelog import default_issue_url
from foxy_project.changelog.domain_model import Changelog
from foxy_project.changelog.domain_model import RepositoryInterface
from foxy_project.changelog.domain_model import calendar_nammed_regex
from foxy_project.changelog.domain_model import semver_nammed_regex


if TYPE_CHECKING:
    from git.objects import Commit


class TagPattern(StrEnum):
    SEMVER = "semver"
    CALENDAR = "calendar"


class GitRepository(RepositoryInterface):  # pylint: disable=too-few-public-methods
    def __init__(  # pylint: disable=too-many-arguments
        self,
        repository_path,
        latest_version: str | None = None,
        skip_unreleased: bool = True,
        tag_prefix: str = "",
        tag_pattern: str = "semver",
    ):
        self.repository = Repo(repository_path)
        self.tag_prefix = tag_prefix
        self.tag_pattern = tag_pattern
        self.commit_tags_index = self._init_commit_tags_index(self.repository, self.tag_prefix, self.tag_pattern)
        # in case of defined latest version, unreleased is used as latest release
        self._skip_unreleased = skip_unreleased and not bool(latest_version)
        self._latest_version = latest_version or None

    def generate_changelog(  # pylint: disable=too-many-arguments,too-many-locals
        self,
        title: str = "Changelog",
        description: str = "",
        remote: str = "origin",
        issue_pattern: str | None = None,
        issue_url: str | None = None,
        diff_url: str | None = None,
        starting_commit: str = "",
        stopping_commit: str = "HEAD",
    ) -> Changelog:
        locallogger = logging.getLogger("repository.generate_changelog")
        issue_url = issue_url or self._issue_from_git_remote_url(remote)
        diff_url = diff_url or self._diff_from_git_remote_url(remote)
        changelog = Changelog(title, description, issue_pattern, issue_url, self.tag_prefix, self.tag_pattern)
        if self._repository_is_empty():
            locallogger.info("Repository is empty.")
            return changelog
        iter_rev = self._get_iter_rev(starting_commit, stopping_commit)
        commits = self.repository.iter_commits(
            iter_rev, topo_order=True
        )  # Fixes this bug: https://github.com/KeNaCo/auto-changelog/issues/112
        # Some thoughts here
        #  First we need to check if all commits are "released". If not, we have to create our special "Unreleased"
        #  release. Then we simply iter over all commits, assign them to current release or create new if we find it.
        first_commit = True
        skip = self._skip_unreleased
        locallogger.debug("Start iterating commits")
        for commit in commits:
            sha = commit.hexsha[0:7]
            locallogger.debug("Found commit %s", sha)

            if skip and commit not in self.commit_tags_index:
                locallogger.debug("Skipping unreleased commit %s", sha)
                continue
            skip = False

            if first_commit and commit not in self.commit_tags_index:
                # if no last version specified by the user => consider HEAD
                if not self._latest_version:
                    locallogger.debug("Adding release 'unreleased'")
                    changelog.add_release("Unreleased", sha, date.today(), sha256())
                else:
                    locallogger.debug("Adding release '%s'", self._latest_version)
                    changelog.add_release(self._latest_version, self._latest_version, date.today(), sha256())
            first_commit = False

            if commit in self.commit_tags_index:
                release_attributes = self._extract_release_args(commit, self.commit_tags_index[commit])
                locallogger.debug("Adding release '%s' with attributes %s", release_attributes[0], release_attributes)
                changelog.add_release(*release_attributes)

            note_attributes = self._extract_note_args(commit)
            locallogger.debug("Adding commit %s with attributes %s", sha, note_attributes)
            changelog.add_note(*note_attributes)

        # create the compare url for each release
        releases = changelog.releases
        # we are using len(changelog.releases) - 1 because there is not compare url for the oldest version
        if diff_url is not None:  # if links are off
            for release_index in reversed(range(len(changelog.releases) - 1)):
                releases[release_index].set_compare_url(diff_url, releases[release_index + 1].title)

        # Close the link to the repository
        # If we are not closing it, some references are not cleaned on windows
        self.repository.close()

        return changelog

    def _issue_from_git_remote_url(self, remote: str) -> Optional[str]:
        """Creates issue url with {id} format key"""
        try:
            url = self._remote_url(remote)
            return default_issue_url.format(base_url=url)
        except ValueError as e:
            logging.error("%s. Turning off issue links.", e)
            return None

    def _diff_from_git_remote_url(self, remote: str):
        try:
            url = self._remote_url(remote)
            return default_diff_url.format(base_url=url)
        except ValueError as e:
            logging.error("%s. Turning off compare url links.", e)
            return None

    def _remote_url(self, remote: str) -> str:
        """Extract remote url from remote url"""
        url = self._get_git_url(remote=remote)
        url = GitRepository._sanitize_remote_url(url)
        return url

    @staticmethod
    def _sanitize_remote_url(remote: str) -> str:
        # 'git@github.com:Michael-F-Bryan/auto-changelog.git' -> 'https://github.com/Michael-F-Bryan/auto-changelog'
        # 'https://github.com/Michael-F-Bryan/auto-changelog.git' -> 'https://github.com/Michael-F-Bryan/auto-changelog'
        return re.sub(r"^(https|git|ssh)(:\/\/|@)(.*@)?([^\/:]+)[\/:]([^\/:]+)\/(.+).git$", r"https://\4/\5/\6", remote)

    # This part is hard to mock, separate method is nice approach how to overcome this problem
    def _get_git_url(self, remote: str) -> str:
        remote_config = self.repository.remote(name=remote).config_reader
        # remote url can be in one of this three options
        # Test is the option exits before access it, otherwise the program crashes
        if remote_config.has_option("url"):
            return remote_config.get("url")
        elif remote_config.has_option("pushurl"):
            return remote_config.get("pushurl")
        elif remote_config.has_option("pullurl"):
            return remote_config.get("pullurl")
        else:
            return ""

    def _get_iter_rev(self, starting_commit: str, stopping_commit: str):
        if starting_commit:
            c = self.repository.commit(starting_commit)
            if not c.parents:
                # starting_commit is initial commit,
                # treat as default
                starting_commit = ""
            else:
                # iter_commits iters from the first rev to the second rev,
                # but not contains the second rev.
                # Here we set the second rev to its previous one then the
                # second rev would be included.
                starting_commit = f"{starting_commit}~1"

        iter_rev = f"{stopping_commit}...{starting_commit}" if starting_commit else stopping_commit
        return iter_rev

    def _repository_is_empty(self):
        return not bool(self.repository.references)

    @staticmethod
    def _init_commit_tags_index(
        repo: Repo, tag_prefix: str, tag_pattern: str = "semver"
    ) -> dict[Commit, list[TagReference]]:
        """Create reverse index"""
        reverse_tag_index: dict[Commit, list[TagReference]] = {}
        for tagref in repo.tags:
            tag_name = tagref.name
            commit = tagref.commit

            consider_tag = False

            # consider & remove the prefix if we found one
            if tag_name.startswith(tag_prefix):
                tag_name = tag_name.replace(tag_prefix, "")

                if (tag_pattern == TagPattern.SEMVER and re.fullmatch(semver_nammed_regex, tag_name)) or (  # noqa: SIM114
                    tag_pattern == TagPattern.CALENDAR and re.fullmatch(calendar_nammed_regex, tag_name)
                ):
                    consider_tag = True
                elif re.fullmatch(tag_pattern, tag_name):
                    consider_tag = True
            # good format of the tag => consider it
            if consider_tag:
                if commit not in reverse_tag_index:
                    reverse_tag_index[commit] = []
                reverse_tag_index[commit].append(tagref)
        return reverse_tag_index

    @staticmethod
    def _extract_release_args(commit, tags) -> tuple[str, str, Any, Any]:
        """Extracts arguments for release"""
        title = ", ".join(map(lambda tag: f"{tag.name}", tags))
        date_ = commit.authored_datetime.date()
        sha = commit.hexsha

        # TODO parse message, be carefull about commit message and tags message

        return title, title, date_, sha

    @staticmethod
    def _extract_note_args(commit) -> tuple[str, str, str, str, str, str]:
        """Extracts arguments for release Note from commit"""
        sha = commit.hexsha
        message = commit.message
        type_, scope, description, body, footer = GitRepository._parse_conventional_commit(message)
        return sha, type_, description, scope, body, footer

    @staticmethod
    def _parse_conventional_commit(message: str) -> tuple[str, str, str, str, str]:
        type_ = scope = description = body_footer = body = footer = ""
        # TODO this is less restrictive version of re. I have somewhere more restrictive one, maybe as option?
        match = re.match(r"^(\w+)(\([\w\-.]+\))?!?: (.*)(\n\n[\w\W]*)?$", message.strip())
        if match:
            type_, scope, description, body_footer = match.groups(default="")
        else:
            locallogger = logging.getLogger("repository._parse_conventional_commit")
            locallogger.debug("Commit message did not match expected pattern: %s", message)
        if scope:
            scope = scope[1:-1]
        if body_footer:
            bf_match = re.match(r"^(\n\n[\w\W]+?)?(\n\n([a-zA-Z-]+|BREAKING[- ]CHANGE)(: | #)[\w\W]+)$", body_footer)
            if bf_match:
                result = bf_match.groups(default="")
                body = result[0][2:]
                footer = result[1][2:]
            else:
                body = body_footer[2:]
        return type_, scope, description, body, footer
