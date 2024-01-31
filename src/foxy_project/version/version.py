from __future__ import annotations

import click

from setuptools_scm import get_version


@click.command(help="View project's version based on the commit history.")
def version() -> None:
    click.echo(f"{get_version()}")
