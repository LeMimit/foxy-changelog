# SPDX-FileCopyrightText: 2024-present Fabien Hermitte
#
# SPDX-License-Identifier: MIT


from __future__ import annotations

import click

from foxy_project._version import __version__
from foxy_project.changelog.changelog import changelog
from foxy_project.version.version import version


@click.group()
@click.version_option(version=__version__, prog_name="Foxy project")
def cli() -> None:
    pass


cli.add_command(changelog)
cli.add_command(version)
