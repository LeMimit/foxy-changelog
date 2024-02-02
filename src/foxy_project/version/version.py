# SPDX-FileCopyrightText: 2010-2024 Ronny Pfannschmidt <opensource@ronnypfannschmidt.de>
# SPDX-FileCopyrightText: 2024-present Fabien Hermitte
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import os

from pathlib import Path
from typing import Iterator

import click

from setuptools_scm import get_version

from foxy_project.config.pyproject_reading import FOXY_PROJECT_TOML
from foxy_project.config.pyproject_reading import PYPROJECT
from foxy_project.version._config import Configuration


@click.command(help="View project's version based on the commit history.")
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True),
    default=None,
    help="path to 'pyproject.toml' with foxy-project config or 'foxy-project.toml' , "
    "default: looked up in the current or parent directories",
)
@click.option(
    "-p",
    "--path-repo",
    type=click.Path(exists=True),
    default=".",
    help="Path to the repository's root directory [Default: .]",
)
@click.option(
    "--version-scheme",
    type=str,
    default=None,
    help="Configures how the local version number is constructed;"
    "either an entrypoint name or a callable. [Default: semver-conventional-commit-foxy]",
)
@click.option(
    "--local-scheme",
    type=str,
    default=None,
    help="Configures how the local version number is constructed;"
    "either an entrypoint name or a callable. [Default: node-and-date]",
)
@click.option(
    "--version-file",
    type=click.Path(exists=True),
    default=None,
    help="A path to a file that gets replaced with a file containing the current version.",
)
@click.option(
    "--version-file-template",
    type=str,
    default=None,
    help="A new-style format string that is given the current"
    "version as the version keyword argument for formatting.",
)
@click.option(
    "--relative-to",
    type=click.Path(exists=True),
    default=None,
    help="A file/directory from which the root can be resolved.",
)
@click.option(
    "--tag-regex",
    type=str,
    default=None,
    help="A Python regex string to extract the version part from any SCM tag."
    "The regex needs to contain either a single match group, or a group named version,"
    "that captures the actual version information.",
)
@click.option(
    "--parentdir-prefix-version",
    type=str,
    default=None,
    help="If the normal methods for detecting the version (SCM version, sdist metadata) fail,"
    "and the parent directory name starts with parentdir_prefix_version,"
    "then this prefix is stripped and the rest of the parent directory name"
    "is matched with tag_regex to get a version string.",
)
@click.option(
    "--fallback-version",
    type=str,
    default=None,
    help="A version string that will be used if no other method for detecting the version worked"
    "(e.g., when using a tarball with no metadata).",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="set logging level to DEBUG",
)
def version(
    config: click.Path | None,
    path_repo: click.Path,
    version_scheme: str | None,
    local_scheme: str | None,
    version_file: click.Path | None,
    version_file_template: str | None,
    relative_to: click.Path | None,
    tag_regex: str | None,
    parentdir_prefix_version: str | None,
    fallback_version: str | None,
    debug: bool | None,
) -> None:
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Logging level has been set to DEBUG")

    # Priority to find configuration file user configuration -> foxy-project.toml -> pyproject.toml
    config_file = (
        config or _find_file(str(path_repo), name=FOXY_PROJECT_TOML) or _find_file(str(path_repo), name=PYPROJECT)
    )

    configuration = (
        Configuration.from_file(str(config_file), root=os.path.abspath(str(path_repo)))
        if config_file is not None
        else Configuration()
    )
    # Configurations from command line override configuration from file
    configuration = configuration.copy(
        {
            "version_scheme": version_scheme,
            "local_scheme": local_scheme,
            "version_file": Path(str(version_file)) if version_file is not None else None,
            "version_file_template": version_file_template,
            "relative_to": Path(str(relative_to)) if relative_to is not None else None,
            "tag_regex": tag_regex,
            "parentdir_prefix_version": parentdir_prefix_version,
            "fallback_version": fallback_version,
        }
    )

    version = get_version(
        root=configuration.root,
        version_scheme=configuration.version_scheme,
        local_scheme=configuration.local_scheme,
        version_file=configuration.version_file,
        version_file_template=configuration.version_file_template,
        relative_to=configuration.relative_to,
        tag_regex=configuration.tag_regex,
        fallback_version=configuration.fallback_version,
        normalize=configuration.normalize,
    )
    click.echo(version)


def _find_file(parent: str, name: str) -> str | None:
    for directory in _walk_potential_roots(os.path.abspath(parent)):
        pyproject = os.path.join(directory, name)
        if os.path.isfile(pyproject):
            return pyproject

    return None


def _walk_potential_roots(root: str, *, search_parents: bool = True) -> Iterator[Path]:
    """
    Iterate though a path and each of its parents.
    :param root: File path.
    :param search_parents: If ``False`` the parents are not considered.
    """
    root_path = Path(root)
    yield root_path
    if search_parents:
        yield from root_path.parents
