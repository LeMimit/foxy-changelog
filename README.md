# 🦊 Foxy changelog

> [!IMPORTANT]
> This repository is a fork of [auto-changelog](https://github.com/KeNaCo/auto-changelog).
> I decided to do it because auto-changelog is not maintained anymore and I need some changes for my personal usage.
> I will publish these changes for everyone to use but I do not promise to answer to feature request and bug fixes.
>
> **Sadly I do not have time to provide steps to contribute and not everything will be tested.**

A quick script that will generate a changelog for any git repository using [`conventional style`](https://www.conventionalcommits.org/en/v1.0.0/) commit messages.

## Installation

It is recommanded to install this tool with [`pipx`](https://github.com/pypa/pipx) to install it in a isolated environments:

```console
pipx install foxy-changelog
```

## Command line interface

You can list the command line options by running `foxy-changelog --help`:

```console
Usage: foxy-changelog [OPTIONS]

Options:
-p, --path-repo PATH       Path to the repository's root directory
                           [Default: .]

-t, --title TEXT           The changelog's title [Default: Changelog]
-d, --description TEXT     Your project's description
-o, --output FILENAME      The place to save the generated changelog
                           [Default: CHANGELOG.md]

-r, --remote TEXT          Specify git remote to use for links
-v, --latest-version TEXT  use specified version as latest release
-u, --unreleased           Include section for unreleased changes
--template TEXT            specify template to use [compact] or a path to a
                           custom template, default: compact

--diff-url TEXT            override url for compares, use {current} and
                           {previous} for tags

--issue-url TEXT           Override url for issues, use {id} for issue id
--issue-pattern TEXT       Override regex pattern for issues in commit
                           messages. Should contain two groups, original
                           match and ID used by issue-url.

--tag-pattern TEXT         override regex pattern for release tags. By
                           default use semver tag names semantic. tag should
                           be contain in one group named 'version'.

--tag-prefix TEXT          prefix used in version tags, default: ""
--stdout
--tag-pattern TEXT         Override regex pattern for release tags
--starting-commit TEXT     Starting commit to use for changelog generation
--stopping-commit TEXT     Stopping commit to use for changelog generation
--debug                    set logging level to DEBUG
--help                     Show this message and exit.
```

## Version management

`foxy-changelog` is providing support to automatically generate the version of your project according to commit history.

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

To manage the version with a version based on the calendar. The supported convention is YYYY.MM.Patch with Patch a number not 0-padded starting to 1. (example: 2024.01.1).

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
