from __future__ import annotations

import logging
import os

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import Iterator

import click

from foxy_changelog import set_github
from foxy_changelog import set_gitlab
from foxy_changelog._config import FOXY_CHANGELOG_TOML
from foxy_changelog._config import PYPROJECT
from foxy_changelog._config import Configuration
from foxy_changelog.presenter import MarkdownPresenter
from foxy_changelog.presenter import default_template
from foxy_changelog.repository import GitRepository


if TYPE_CHECKING:
    from foxy_changelog.domain_model import PresenterInterface
    from foxy_changelog.domain_model import RepositoryInterface


def validate_template(ctx: Any, param: Any, value: str | None) -> str | None:  # noqa: ARG001
    # Check if an embedded template is passed in parameter or a jinja2 file
    if value is None or (value in default_template or value.endswith(".jinja2")):
        return value

    msg = "Need to pass an embedded template name or a .jinja2 file"
    raise click.BadParameter(msg)


def generate_changelog(
    repository: RepositoryInterface, presenter: PresenterInterface, *args: Any, **kwargs: Any
) -> str:
    """Use-case function coordinates repository and interface"""
    changelog = repository.generate_changelog(*args, **kwargs)
    return presenter.present(changelog)


@click.command()
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True),
    default=None,
    help="path to 'pyproject.toml' with foxy-changelog config or 'foxy-changelog.toml' , "
    "default: looked up in the current or parent directories",
)
@click.option(
    "--gitlab",
    help="Set Gitlab Pattern Generation.",
    is_flag=True,
    default=None,
)
@click.option(
    "--github",
    help="Set GitHub Pattern Generation.",
    is_flag=True,
    default=None,
)
@click.option(
    "-p",
    "--path-repo",
    type=click.Path(exists=True),
    default=".",
    help="Path to the repository's root directory [Default: .]",
)
@click.option("-t", "--title", default=None, type=str, help="The changelog's title [Default: Changelog]")
@click.option("-d", "--description", default=None, type=str, help="Your project's description")
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=True),
    default=None,
    help="The place to save the generated changelog [Default: CHANGELOG.md]",
)
@click.option("-r", "--remote", type=str, default=None, help="Specify git remote to use for links")
@click.option("-v", "--latest-version", type=str, default=None, help="use specified version as latest release")
@click.option("-u", "--unreleased", is_flag=True, default=None, help="Include section for unreleased changes")
@click.option(
    "--template",
    callback=validate_template,
    type=str,
    default=None,
    help="specify template to use [compact, lastrelease] or a path to a custom template, default: compact",
)
@click.option(
    "--diff-url", type=str, default=None, help="override url for compares, use {current} and {previous} for tags"
)
@click.option("--issue-url", type=str, default=None, help="Override url for issues, use {id} for issue id")
@click.option(
    "--issue-pattern",
    type=str,
    default=None,
    help="Override regex pattern for issues in commit messages. Should contain two groups, original match and ID used "
    "by issue-url.",
)
@click.option(
    "--tag-pattern",
    type=str,
    default=None,
    help="Specify regex pattern for version tags [semver, calendar, custom-regex]."
    " A custom regex containing one group named 'version' can be specified.",
    show_default=True,
)
@click.option("--tag-prefix", type=str, default=None, help='prefix used in version tags, default: "" ')
@click.option(
    "--stdout",
    is_flag=True,
    default=None,
)
@click.option("--starting-commit", type=str, help="Starting commit to use for changelog generation", default=None)
@click.option("--stopping-commit", type=str, help="Stopping commit to use for changelog generation", default=None)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="set logging level to DEBUG",
)
def main(
    config: click.Path | None,
    path_repo: click.Path,
    gitlab: bool | None,
    github: bool | None,
    title: str | None,
    description: str | None,
    output: click.Path | None,
    remote: str | None,
    latest_version: str | None,
    unreleased: bool | None,
    template: str | None,
    diff_url: str | None,
    issue_url: str | None,
    issue_pattern: str | None,
    tag_prefix: str | None,
    stdout: bool | None,
    tag_pattern: str | None,
    starting_commit: str | None,
    stopping_commit: str | None,
    debug: bool | None,
) -> None:
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Logging level has been set to DEBUG")

    # Priority to find configuration file user configuration -> foxy-changelog.toml -> pyproject.toml
    config_file = (
        config or _find_file(str(path_repo), name=FOXY_CHANGELOG_TOML) or _find_file(str(path_repo), name=PYPROJECT)
    )

    configuration = (
        Configuration.from_file(str(config_file), root=os.path.abspath(str(path_repo)))
        if config_file is not None
        else Configuration()
    )
    # Configurations from command line override configuration from file
    configuration = configuration.copy(
        {
            "gitlab": gitlab,
            "github": github,
            "title": title,
            "description": description,
            "output": Path(str(output)) if output is not None else None,
            "remote": remote,
            "latest_version": latest_version,
            "unreleased": unreleased,
            "template": template,
            "diff_url": diff_url,
            "issue_url": issue_url,
            "issue_pattern": issue_pattern,
            "tag_prefix": tag_prefix,
            "stdout": stdout,
            "tag_pattern": tag_pattern,
            "starting_commit": starting_commit,
            "stopping_commit": stopping_commit,
        }
    )

    if configuration.gitlab:
        set_gitlab()

    if configuration.github:
        set_github()

    # Convert the repository name to an absolute path
    repo = os.path.abspath(str(path_repo))

    repository = GitRepository(
        repo,
        latest_version=configuration.latest_version,
        skip_unreleased=not configuration.unreleased,
        tag_prefix=configuration.tag_prefix,
        tag_pattern=configuration.tag_pattern,
    )
    presenter = MarkdownPresenter(template=configuration.template)
    changelog = generate_changelog(
        repository,
        presenter,
        title=configuration.title,
        description=configuration.description,
        remote=configuration.remote,
        issue_pattern=configuration.issue_pattern,
        issue_url=configuration.issue_url,
        diff_url=configuration.diff_url,
        starting_commit=configuration.starting_commit,
        stopping_commit=configuration.stopping_commit,
    )

    if stdout:
        print(changelog)  # noqa: T201
    else:
        _write_changelog(output=configuration.output, changelog=changelog)


PATTERN = "<!-- foxy-changelog-above -->"


def _write_changelog(output: Path, changelog: Any) -> None:
    with open(output, "r+b") as output_file:
        lines = [line.decode("utf-8").rstrip() for line in output_file]
        kept_lines: list[str] = []
        is_pattern_found = False
        # Kept the lines after the pattern
        for line in lines:
            if is_pattern_found:
                kept_lines.append(line)
            if PATTERN in line:
                is_pattern_found = True
                kept_lines.append(line)
        # Remove all the content of the file
        output_file.seek(0)
        output_file.truncate()
        # First writes the new generated changelog
        # Second if some lines are kept, writes it back after the generated changelog
        output_file.write(changelog.encode("utf-8"))
        if len(kept_lines) > 0:
            output_file.write(b"\n")
            for line in kept_lines:
                output_file.write(f"{line}\n".encode())


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
