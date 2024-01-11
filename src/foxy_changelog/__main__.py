from __future__ import annotations

import logging
import os

from typing import TYPE_CHECKING
from typing import Any

import click

from foxy_changelog import set_github
from foxy_changelog import set_gitlab
from foxy_changelog.presenter import MarkdownPresenter
from foxy_changelog.presenter import default_template
from foxy_changelog.repository import GitRepository


if TYPE_CHECKING:
    from foxy_changelog.domain_model import PresenterInterface
    from foxy_changelog.domain_model import RepositoryInterface


def validate_template(ctx: Any, param: Any, value: str) -> str:  # noqa: ARG001
    # Check if an embedded template is passed in parameter or a jinja2 file
    if value in default_template or value.endswith(".jinja2"):
        return value

    msg = "Need to pass an embedded template name or a .jinja2 file"
    raise click.BadParameter(msg)


def generate_changelog(
    repository: RepositoryInterface, presenter: PresenterInterface, *args: Any, **kwargs: Any
) -> Any:
    """Use-case function coordinates repository and interface"""
    changelog = repository.generate_changelog(*args, **kwargs)
    return presenter.present(changelog)


@click.command()
@click.option("--gitlab", help="Set Gitlab Pattern Generation.", is_flag=True)
@click.option("--github", help="Set GitHub Pattern Generation.", is_flag=True)
@click.option(
    "-p",
    "--path-repo",
    type=click.Path(exists=True),
    default=".",
    help="Path to the repository's root directory [Default: .]",
)
@click.option("-t", "--title", default="Changelog", help="The changelog's title [Default: Changelog]")
@click.option("-d", "--description", help="Your project's description")
@click.option(
    "-o",
    "--output",
    type=click.File("w"),
    default="CHANGELOG.md",
    help="The place to save the generated changelog [Default: CHANGELOG.md]",
)
@click.option("-r", "--remote", default="origin", help="Specify git remote to use for links")
@click.option("-v", "--latest-version", type=str, help="use specified version as latest release")
@click.option("-u", "--unreleased", is_flag=True, default=False, help="Include section for unreleased changes")
@click.option(
    "--template",
    callback=validate_template,
    default="compact",
    help="specify template to use [compact] or a path to a custom template, default: compact ",
)
@click.option("--diff-url", default=None, help="override url for compares, use {current} and {previous} for tags")
@click.option("--issue-url", default=None, help="Override url for issues, use {id} for issue id")
@click.option(
    "--issue-pattern",
    default=r"(#([\w-]+))",
    help="Override regex pattern for issues in commit messages. Should contain two groups, original match and ID used "
    "by issue-url.",
)
@click.option(
    "--tag-pattern",
    default=None,
    help="override regex pattern for release tags. "
    "By default use semver tag names semantic. "
    "tag should be contain in one group named 'version'.",
)
@click.option("--tag-prefix", default="", help='prefix used in version tags, default: "" ')
@click.option("--stdout", is_flag=True)
@click.option("--tag-pattern", default=None, help="Override regex pattern for release tags")
@click.option("--starting-commit", help="Starting commit to use for changelog generation", default="")
@click.option("--stopping-commit", help="Stopping commit to use for changelog generation", default="HEAD")
@click.option(
    "--debug",
    is_flag=True,
    help="set logging level to DEBUG",
)
def main(
    path_repo: str,
    gitlab: str,
    github: str,
    title: str,
    description: str,
    output: Any,
    remote: str,
    latest_version: str,
    unreleased: bool,  # noqa: FBT001
    template: str,
    diff_url: str,
    issue_url: str,
    issue_pattern: str,
    tag_prefix: str,
    stdout: bool,  # noqa: FBT001
    tag_pattern: str | None,
    starting_commit: str,
    stopping_commit: str,
    debug: bool,  # noqa: FBT001
) -> None:
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Logging level has been set to DEBUG")

    if gitlab:
        set_gitlab()

    if github:
        set_github()

    # Convert the repository name to an absolute path
    repo = os.path.abspath(path_repo)

    repository = GitRepository(
        repo,
        latest_version=latest_version,
        skip_unreleased=not unreleased,
        tag_prefix=tag_prefix,
        tag_pattern=tag_pattern,
    )
    presenter = MarkdownPresenter(template=template)
    changelog = generate_changelog(
        repository,
        presenter,
        title,
        description,
        remote=remote,
        issue_pattern=issue_pattern,
        issue_url=issue_url,
        diff_url=diff_url,
        starting_commit=starting_commit,
        stopping_commit=stopping_commit,
    )

    if stdout:
        print(changelog)  # noqa: T201
    else:
        output.write(changelog)
