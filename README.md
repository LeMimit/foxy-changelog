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

You can list the command line options by running `auto-changelog --help`:

```console
Usage: auto-changelog [OPTIONS]

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
