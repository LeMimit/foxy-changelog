# 🦊 Foxy changelog

> [!IMPORTANT]
> This repository is a fork of [auto-changelog](https://github.com/KeNaCo/auto-changelog).
> I decided to do it because auto-changelog is not maintained anymore and I need some changes for my personal usage.
> I will publish these changes for everyone to use but I do not promise to answer to feature request and bug fixes.
>
> **Sadly I do not have time to provide steps to contribute and not everything will be tested.**

A tool which generates a changelog and manage version for any git repository using [`conventional commits`](https://www.conventionalcommits.org/en/v1.0.0/) specification.

- [Installation](#installation)
- [Changelog generation](#changelog-generation)
  - [Add to an existing changelog](#add-to-an-existing-changelog)
- [Version management](#version-management)
  - [semver-conventional-commit-foxy](#semver-conventional-commit-foxy)
  - [calendar-conventional-commit-foxy](#calendar-conventional-commit-foxy)
  - [Hatch](#hatch)
- [Configuration](#configuration)
  - [Python project](#python-project)
  - [Other projects](#other-projects)
- [Command line interface](#command-line-interface)

## Installation

It is recommanded to install this tool with [`pipx`](https://github.com/pypa/pipx) to install it in a isolated environments:

```console
pipx install foxy-changelog
```

## Changelog generation

### Add to an existing changelog

If you’d like to keep an existing changelog below your generated one, just add `<!-- foxy-changelog-above -->` to your current changelog.
The generated changelog will be added above this token, and anything below will remain.

> [!TIP]
> This is quite useful when changing the tag pattern (e.g. from semver to calendar) used to version a project or to help keeping an old manually generated changelog when integrated conventional commit to a project to integrate foxy-changelog.

## Version management

`foxy-changelog` is providing support to automatically generate the version of your python project according to its commit history.

The management is based on [setuptools_scm](https://github.com/pypa/setuptools_scm) and [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/).

As defined in the conventional commit specification:

>- The type `feat` MUST be used when a commit adds a new feature to your application or library.
>- The type `fix` MUST be used when a commit represents a bug fix for your application.

`foxy-changelog` is providing two entry points for `setuptools_scm.version_scheme` configuration.

### semver-conventional-commit-foxy

Based on [semver](https://semver.org/lang/fr/).

Rules:

- A commit with type `feat` activates an increment of the minor.
- All other types will activate an increment of the patch.

> [!NOTE]
> Breaking changes is not supported yet.

### calendar-conventional-commit-foxy

To manage version based on the calendar. The supported convention is YYYY.MM.Patch with Patch a number not 0-padded starting to 1. (example: 2024.01.1).

Rules:

- A commit with type `feat` activates an increment of the month.
- All other types will activate an increment of the patch version.
- The year is automatically incremented at the end a year.

### Hatch

[Hatch](https://github.com/pypa/hatch) is supporting out of the box thanks to [hatch-vcs](https://github.com/ofek/hatch-vcs).
Python projet using other project management tool can use `setuptools_scm` directly.

Ensure `hatch-vcs` and `foxy-changelog` is defined within the `build-system.requires` field in your `pyproject.toml` file.

All other options supported by `hatch-vcs` and `setuptools_scm` can be used. More information can be found in their documentation.

```toml
[build-system]
requires = ["hatchling", "hatch-vcs", "foxy-changelog"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"

[tool.hatch.version.raw-options]
version_scheme = "semver-conventional-commit-foxy"
```

## Configuration

`foxy-changelog` can be configured thanks to its command line or configuration files (`foxy-changelog.toml` or `pyproject.toml`).
All the configurations of the command line to be also put in the configuration files for easier usage.

Configurations files are automatically looked up in the project's folder but custom path can always to passed to the command line.
Configurations from different sources are considered with an defined order.
Commande line options overrides configurations from `foxy-changelog.toml` which overrides configurations from `pyproject.toml`.

### Python project

`pyproject.toml` is supported and is the recommanded way to configure python projects.

The following configuration block can be added to the `pyproject.toml` file.

```toml
[tool.foxy-changelog.changelog]
tag_pattern = "semver"
```

If no title and description are provided the one from `project` configuration are taken.

### Other projects

`foxy-changelog.toml` is recommanded way.

The following configuration block can be added to the `foxy-changelog.toml` file.

```toml
[changelog]
tag_pattern = "semver"
```

## Command line interface

You can list the command line options by running `foxy-changelog --help`:

```console
Usage: foxy-changelog [OPTIONS]

Options:
-c, --config PATH          path to 'pyproject.toml' with foxy-changelog
                           config or 'foxy-changelog.toml' , default: looked
                           up in the current or parent directories
--gitlab                   Set Gitlab Pattern Generation.
--github                   Set GitHub Pattern Generation.
-p, --path-repo PATH       Path to the repository's root directory
                           [Default: .]

-t, --title TEXT           The changelog's title [Default: Changelog]
-d, --description TEXT     Your project's description
-o, --output FILENAME      The place to save the generated changelog
                           [Default: CHANGELOG.md]

-r, --remote TEXT          Specify git remote to use for links
-v, --latest-version TEXT  use specified version as latest release
-u, --unreleased           Include section for unreleased changes
--template TEXT            specify template to use [compact, lastrelease] or a path
                           to a custom template, default: compact

--diff-url TEXT            override url for compares, use {current} and
                           {previous} for tags

--issue-url TEXT           Override url for issues, use {id} for issue id
--issue-pattern TEXT       Override regex pattern for issues in commit
                           messages. Should contain two groups, original
                           match and ID used by issue-url.

--tag-pattern TEXT         Specify regex pattern for version tags [semver,
                           calendar, custom-regex]. A custom regex containing
                           one group named 'version' can be specified.
                           [default: semver]

--tag-prefix TEXT          prefix used in version tags, default: ""
--stdout
--tag-pattern TEXT         Override regex pattern for release tags
--starting-commit TEXT     Starting commit to use for changelog generation
--stopping-commit TEXT     Stopping commit to use for changelog generation
--debug                    set logging level to DEBUG
--help                     Show this message and exit.
```
