# 🦊 Foxy project

> [!IMPORTANT]
> This repository is a fork of [auto-changelog](https://github.com/KeNaCo/auto-changelog).
> I decided to do it because auto-changelog is not maintained anymore and I need some changes for my personal usage.
> I will publish these changes for everyone to use but I do not promise to answer to feature request and bug fixes.
>
> **Sadly I do not have time to provide steps to contribute and not everything will be tested.**

| | |
| --- | --- |
| Package    |  [![PyPI - Version](https://img.shields.io/pypi/v/foxy-project.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/foxy-project/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/foxy-project.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/foxy-project/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/foxy-project.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/foxy-project/)  |
| Meta   | [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/)  |

A tool which generates a changelog and manage version for any git repository using [`conventional commits`](https://www.conventionalcommits.org/en/v1.0.0/) specification.

- [Installation](#installation)
- [Changelog generation](#changelog-generation)
  - [Add to an existing changelog](#add-to-an-existing-changelog)
- [Version management](#version-management)
  - [pep440-conventional-commit-foxy](#pep440-conventional-commit-foxy)
  - [semver-conventional-commit-foxy](#semver-conventional-commit-foxy)
  - [calendar-conventional-commit-foxy](#calendar-conventional-commit-foxy)
- [Configuration](#configuration)
  - [Python project](#python-project)
  - [Hatch](#hatch)
  - [Other projects](#other-projects)
  - [Available configurations](#available-configurations)
- [Github actions sdsd](#github-actions-sdsd)
- [Command line interface](#command-line-interface)
  - [foxy-project changelog](#foxy-project-changelog)
  - [foxy-project version](#foxy-project-version)

## Installation

It is recommanded to install this tool with [`pipx`](https://github.com/pypa/pipx) to install it in a isolated environments:

```console
pipx install foxy-project
```

## Changelog generation

Runnning the following command in the working environment will generate the project's changelog according to its commit history.

```console
foxy-project changelog
```

### Add to an existing changelog

If you’d like to keep an existing changelog below your generated one, just add `<!-- foxy-changelog-above -->` to your current changelog.
The generated changelog will be added above this token, and anything below will remain.

> [!TIP]
> This is quite useful when changing the tag pattern (e.g. from semver to calendar) used to version a project or to help keeping an old manually generated changelog when integrated conventional commit to a project.

## Version management

`foxy-project` is providing support to automatically generate the version of your python project according to its commit history.

The management is based on [setuptools_scm](https://github.com/pypa/setuptools_scm) and [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/).

As defined in the conventional commit specification:

>- The type `feat` MUST be used when a commit adds a new feature to your application or library.
>- The type `fix` MUST be used when a commit represents a bug fix for your application.

Runnning the following command in the working environment will print the project's version the according to its commit history.

```console
foxy-project version
```

> [!TIP]
> It is also possible to generate a file with the generated version. This behavior is deactivated by default.
>
> Use the `version_file` and `version_file_template` option to configure the generation.
> Embedded templates for `.py` and `.txt` are available. A custom template needs to be provided for other type of file.

`foxy-project` is providing three version schemas which control how the version is incremented.

### pep440-conventional-commit-foxy

Based on [PEP440](https://peps.python.org/pep-0440/). Selected by default.

Logic:

A commit with `feat` type activates an increment of the minor, otherwise all other types will activate an increment of the patch.
Then appends `.devN` where `N` is the distance between the current commit and the previous tag.

> [!WARNING]
> Breaking changes and pre-release is not supported yet.

### semver-conventional-commit-foxy

Based on [semver](https://semver.org/lang/fr/).

Logic:

A commit with `feat` type activates an increment of the minor, otherwise all other types will activate an increment of the patch.
Then appends `-devN` where `N` is the distance between the current commit and the previous tag.

> [!WARNING]
> Breaking changes and pre-release with other name than `dev` is not supported yet.

### calendar-conventional-commit-foxy

To manage version based on the calendar. Based on ([calver](https://calver.org/)).
The supported convention is YYYY.MM.Patch with Patch a number not 0-padded starting to 1. (example: 2024.01.1).

Logic:

A commit with `feat` type activates an increment of the montg, otherwise all other types will activate an increment of the patch.
The year is automatically incremented at the end a year.
Then appends `.devN` where `N` is the distance between the current commit and the previous tag.

## Configuration

`foxy-project` can be configured thanks to its command line or configuration files (`foxy-project.toml` or `pyproject.toml`).

Configurations files are automatically looked up in the project's folder but custom path can always to passed to the command line.

Configurations from different sources are considered with an defined order.
Commande line options overrides configurations from `foxy-project.toml` which overrides configurations from `pyproject.toml`.

### Python project

`pyproject.toml` is supported and is the recommanded way to configure python projects.

### Hatch

[Hatch](https://github.com/pypa/hatch) is supported out of the box thanks to [hatch-vcs](https://github.com/ofek/hatch-vcs).
Python projet using other project management tool can use `foxy-project` directly.

Ensure `hatch-vcs` and `foxy-project` are defined within the `build-system.requires` field in your `pyproject.toml` file.
All other options supported by `hatch-vcs` can be used. More information can be found in their documentation.

Usure to run `hatch version` instead of `foxy-project version` to avoid conflicts.

Only the version management is integrated into Hatch which will generate the good version at build time.

Changelog generation can be configured into a `tool.foxy-project.changelog` section.
If no title and description are provided for the changelog the one from `project` configuration are taken.

```toml
[build-system]
requires = ["hatchling", "hatch-vcs", "foxy-project"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"

[tool.hatch.version.raw-options]
version_scheme = "semver-conventional-commit-foxy"
local_scheme = "no-local-version"

[tool.foxy-project.changelog]
tag_pattern = "semver"
```

### Other projects

`foxy-project.toml` is the recommanded way.

The following configuration block can be added to the `foxy-project.toml` file.

```toml
[changelog]
tag_pattern = "semver"

[version]
local_scheme = "no-local-version"
```

### Available configurations

```toml

# Changelog configuration

[changelog]
# foxy-project.toml

[tool.foxy-project.changelog]
# pyproject.toml
gitlab=false
github=true
title="Changelog"
description="description"
output="CHANGELOG.md"
remote="origin"
latest_version=""
unreleased=false
template="compact"
diff_url=""
issue_url=""
issue_pattern=""
tag_pattern="semver"
tag_prefix=""
stdout=false
starting_commit=""
stopping_commit="HEAD"

# Version configuration

[version]
# foxy-project.toml


[tool.foxy-project.version]
# pyproject.toml
version_scheme="semver-conventional-commit-foxy"
# See <https://setuptools-scm.readthedocs.io/en/latest/extending#setuptools_scmlocal_scheme>
local_scheme="node-and-date"
version_file=""
version_file_template=""
relative_to=""
tag_regex=""
parentdir_prefix_version=""
fallback_version=""
```

## Github actions sdsd

This repository is providing two composite actions to help automate release on Github actions:

- `setup-foxy-project` which set up the lastest version of foxy-project and add the command-line tools to the PATH.
- `generate-changelog` which generate the changelog and commit it on a branch.
- `create-release` which create a tag and the github release of a new version.

You can look at the workflows ([prepare-release](https://github.com/LeMimit/foxy-project/blob/7056bde43b0f0b7ce1d315e51225a0394352a8cf/.github/workflows/prepare-release.yml) and [create-release](https://github.com/LeMimit/foxy-project/blob/7056bde43b0f0b7ce1d315e51225a0394352a8cf/.github/workflows/create-release.yml)) of this project to see how to use them.

The advantage of this process is that it does not interfere with the protection of the default branch and no personal PAT needs to be created.

> [!NOTE]
> You need to allow workflows to create pull request in the settings of the repository.

## Command line interface

You can list the command line options by running `foxy-project --help`:

```console
Usage: foxy-project [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  changelog  Generate a changelog based on the commit history.
  version    View project's version based on the commit history.
```

### foxy-project changelog

You can list the options of `foxy-project changelog` by running `foxy-project changelog --help`:

```console
Usage: foxy-project changelog [OPTIONS]

  Generate a changelog based on the commit history.

Options:
  -c, --config PATH          path to 'pyproject.toml' with foxy-project config
                             or 'foxy-project.toml' , default: looked up in
                             the current or parent directories
  --gitlab                   Set Gitlab Pattern Generation.
  --github                   Set GitHub Pattern Generation.
  -p, --path-repo PATH       Path to the repository's root directory [Default:
                             .]
  -t, --title TEXT           The changelog's title [Default: Changelog]
  -d, --description TEXT     Your project's description
  -o, --output PATH          The place to save the generated changelog
                             [Default: CHANGELOG.md]
  -r, --remote TEXT          Specify git remote to use for links
  -v, --latest-version TEXT  use specified version as latest release
  -u, --unreleased           Include section for unreleased changes
  --template TEXT            specify template to use [compact, lastrelease] or
                             a path to a custom template, default: compact
  --diff-url TEXT            override url for compares, use {current} and
                             {previous} for tags
  --issue-url TEXT           Override url for issues, use {id} for issue id
  --issue-pattern TEXT       Override regex pattern for issues in commit
                             messages. Should contain two groups, original
                             match and ID used by issue-url.
  --tag-pattern TEXT         Specify regex pattern for version tags [semver,
                             calendar, custom-regex]. A custom regex
                             containing one group named 'version' can be
                             specified.
  --tag-prefix TEXT          prefix used in version tags, default: ""
  --stdout
  --starting-commit TEXT     Starting commit to use for changelog generation
  --stopping-commit TEXT     Stopping commit to use for changelog generation
  --debug                    set logging level to DEBUG
  --help                     Show this message and exit.
```

### foxy-project version

You can list the options of `foxy-project version` by running `foxy-project version --help`:

```console
Usage: foxy-project version [OPTIONS]

  View project's version based on the commit history.

Options:
  -c, --config PATH               path to 'pyproject.toml' with foxy-project
                                  config or 'foxy-project.toml' , default:
                                  looked up in the current or parent
                                  directories
  -p, --path-repo PATH            Path to the repository's root directory
                                  [Default: .]
  --version-scheme TEXT           Configures how the local version number is
                                  constructed;either an entrypoint name or a
                                  callable. [Default: semver-conventional-
                                  commit-foxy]
  --local-scheme TEXT             Configures how the local version number is
                                  constructed;either an entrypoint name or a
                                  callable. [Default: node-and-date]
  --version-file PATH             A path to a file that gets replaced with a
                                  file containing the current version.
  --version-file-template TEXT    A new-style format string that is given the
                                  currentversion as the version keyword
                                  argument for formatting.
  --relative-to PATH              A file/directory from which the root can be
                                  resolved.
  --tag-regex TEXT                A Python regex string to extract the version
                                  part from any SCM tag.The regex needs to
                                  contain either a single match group, or a
                                  group named version,that captures the actual
                                  version information.
  --parentdir-prefix-version TEXT
                                  If the normal methods for detecting the
                                  version (SCM version, sdist metadata)
                                  fail,and the parent directory name starts
                                  with parentdir_prefix_version,then this
                                  prefix is stripped and the rest of the
                                  parent directory nameis matched with
                                  tag_regex to get a version string.
  --fallback-version TEXT         A version string that will be used if no
                                  other method for detecting the version
                                  worked(e.g., when using a tarball with no
                                  metadata).
  --next                          Use the next possible version instead of the
                                  current one.
  --no-print                      Deactivate the print of the version.
  --no-version-file               Deactivate the generation of the version
                                  file.
  --debug                         set logging level to DEBUG
  --help                          Show this message and exit.
```
