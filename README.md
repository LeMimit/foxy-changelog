# 🦊 Foxy project

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
- [Configuration](#configuration)
  - [Python project](#python-project)
  - [Hatch](#hatch)
  - [Other projects](#other-projects)
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

`foxy-project` is providing two logics which control how the version is incremented.

### semver-conventional-commit-foxy

Based on [semver](https://semver.org/lang/fr/). Selected by default.

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
  --debug                         set logging level to DEBUG
  --help                          Show this message and exit.
```
