# foxy-project

A tool which generates a changelog and manage version for any git repository using conventional commits specification

## 2.2.0

> `2024-02-04`

### Continuous integration 🐹

* **release**: automate publish on pypi ([#58](https://github.com/LeMimit/foxy-project/issues/58))

Full set of changes: [`2.2.0...2.2.0`](https://github.com/LeMimit/foxy-project/compare/2.2.0...2.2.0)

## 2.2.0

> `2024-02-04`

### New features 🚀

* **ci**: provide composite actions to automate release on ci ([#55](https://github.com/LeMimit/foxy-project/issues/55))

### Continuous integration 🐹

* **release**: add workflow to automate release generation ([#56](https://github.com/LeMimit/foxy-project/issues/56))

Full set of changes: [`2.1.0...2.2.0`](https://github.com/LeMimit/foxy-project/compare/2.1.0...2.2.0)

## 2.1.0

> `2024-02-04`

### New features 🚀

* **version**: clearly support semver and pep440 specifications ([#53](https://github.com/LeMimit/foxy-project/issues/53))
* **version**: add options to deactivate feature ([#52](https://github.com/LeMimit/foxy-project/issues/52))
* **version**: make possible to generate the next version ([#51](https://github.com/LeMimit/foxy-project/issues/51))

Full set of changes: [`2.0.0...2.1.0`](https://github.com/LeMimit/foxy-project/compare/2.0.0...2.1.0)

## 2.0.0

> `2024-02-02`

### New features 🚀

* **changelog**: remove version changes into default templates ([#45](https://github.com/LeMimit/foxy-project/issues/45))
* **project**: add --version option ([#42](https://github.com/LeMimit/foxy-project/issues/42))
* **version**: add version command to display project version ([#43](https://github.com/LeMimit/foxy-project/issues/43))

### Fixes 🐞

* **changelog**: create output file if it does not exist ([#33](https://github.com/LeMimit/foxy-project/issues/33))
* **version**: correctly detects type of commit in release ([#40](https://github.com/LeMimit/foxy-project/issues/40))

### Refactorings 🏭

* **project**: add license header to every python files ([#41](https://github.com/LeMimit/foxy-project/issues/41))
* **project**: rename foxy-changelog into foxy-project ([#39](https://github.com/LeMimit/foxy-project/issues/39))

Full set of changes: [`1.2.0...2.0.0`](https://github.com/LeMimit/foxy-project/compare/1.2.0...2.0.0)

## 1.2.0

> `2024-01-27`

### New features 🚀

* **changelog**: add a new template to render only the last release ([#28](https://github.com/LeMimit/foxy-project/issues/28))
* **changelog**: support adding generated changelog to an existing one ([#23](https://github.com/LeMimit/foxy-project/issues/23))
* **changelog**: support semver and calendar tag pattern ([#22](https://github.com/LeMimit/foxy-project/issues/22))
* **conf**: add support of configuration file ([#26](https://github.com/LeMimit/foxy-project/issues/26))

### Fixes 🐞

* **changelog**: apply a better configuration from autoescape ([#30](https://github.com/LeMimit/foxy-project/issues/30))
* **changelog**: improve parsing to consider scope containing - or . ([#25](https://github.com/LeMimit/foxy-project/issues/25))

Full set of changes: [`1.1.0...1.2.0`](https://github.com/LeMimit/foxy-project/compare/1.1.0...1.2.0)

## 1.1.0

> `2024-01-21`

### New features 🚀

* **version**: add version management support ([#15](https://github.com/LeMimit/foxy-project/issues/15))

### Fixes 🐞

* **commit**: add missing import ([#16](https://github.com/LeMimit/foxy-project/issues/16))

### Continuous integration 🐹

* **python**: remove unused and not working workflow ([#17](https://github.com/LeMimit/foxy-project/issues/17))

Full set of changes: [`1.0.0...1.1.0`](https://github.com/LeMimit/foxy-project/compare/1.0.0...1.1.0)

## 1.0.0

> `2024-01-17`

### New features 🚀

* **commit**: support new types - deps, tools and version ([#6](https://github.com/LeMimit/foxy-project/issues/6))
* **template**: display dependency updates as table when possible ([#12](https://github.com/LeMimit/foxy-project/issues/12))
* **template**: sort scope in generated changelog ([#10](https://github.com/LeMimit/foxy-project/issues/10))
* **template**: improve default template ([#8](https://github.com/LeMimit/foxy-project/issues/8))

### Docs 📚

* **readme**: update readme with fork information ([#1](https://github.com/LeMimit/foxy-project/issues/1))
* **template**: add issue and pr templates ([#2](https://github.com/LeMimit/foxy-project/issues/2))

### Tools 🧰

* **hatch**: use hatch as build system ([#4](https://github.com/LeMimit/foxy-project/issues/4))

<!-- foxy-changelog-above -->

<!-- Changelog from https://github.com/KeNaCo/auto-changelog repository -->

## 0.6.0 (2022-11-27)

#### Fixes

* Fixes bug [#112](https://github.com/KeNaCo/auto-changelog/issues/112)
* updated jinja2 / click deps [#113](https://github.com/KeNaCo/auto-changelog/issues/113)

#### Docs

* update readme

#### Others

* Release of version 0.6.0
* update requirements
* set up pre-commit in Gitlab CI
* set up tests in a GitHub actions
* set up pre-commit in a GitHub actions
* update tooling
* drop support for python 3.6
* (poetry): update locked dependencies
* (poetry): update pyproject.toml to use poetry.groups
* black

Full set of changes: [`0.5.3...0.6.0`](https://gitlab.com/KeNaCo/auto-changelog/compare/0.5.3...0.6.0)

## 0.5.3 (2021-04-13)

#### New Features

* add support gitlab
* add support of custom template (--template)
* Adding debug messages for commit parsing/changelog generation
* Add debug mode

#### Fixes

* default_issue_pattern
* (tests): Prevent GPG pass and sing issues
* (tests): Failing double line test expects link
* change option from --repo to --path-repo
* (regex): accept empty additional commit body
* (git): clean references after process
* sanitaztion of remote url
* Improve parsing of conventional commits by considering breaking changes
* Handling of multiline bodies and footer

#### Refactorings

* (tests): Replace parcial asserts with full content comparison
* (tests): Replace files with --allow-empty parameter for commit
* computation of remote url

#### Docs

* Update "Contributing" section in README to cover usage of make and pre-commit
* Add usage section and command line options to README

#### Others

* Add Makefile for build automation
* Add tox for local multi environment testing
* Add pre-commit and hooks for black and flake8
* Add flake8 as linter
* Add dependency to black for dev environment
* Release of version 0.5.3
* (flake8): remove unused import
* Add sandbox folder to gitignore
* (python): drop python 3.5, add support for python 3.9
* (black): fix unsupported py39 target
* fix flakes complains
* Remove unused import
* Line-break long strings
* Use raw string for regex pattern
* Run black on previous PR
* add invalid template  finle name test
* Small improvements in multiple tests
* Add more tests for default remote
* Add notes from JS implementation cross testing
* add integration and unit testing
* refactor integration test
* remove xfail markers from integration tests
* Add integration tests for issue [#79](https://gitlab.com/KeNaCo/auto-changelog/issues/79)

Full set of changes: [`0.5.1...0.5.3`](https://gitlab.com/KeNaCo/auto-changelog/compare/0.5.1...0.5.3)

## 0.5.1 (2020-06-20)

#### Fixes

* Missing link feature control for diffs [#74](https://gitlab.com/KeNaCo/auto-changelog/issues/74)

#### Others

* Release of version 0.5.1

Full set of changes: [`0.5.0...0.5.1`](https://gitlab.com/KeNaCo/auto-changelog/compare/0.5.0...0.5.1)

## 0.5.0 (2020-05-31)

#### New Features

* change how is managed compare_url feature
* add --tag-prefix, --tag-pattern and --compare-url options
* Add --tag-pattern option [#19](https://gitlab.com/KeNaCo/auto-changelog/issues/19) (credit to @LeMimit)

#### Fixes

* test_tag_pattern works for all py versions
* change compare_url to diff_url
* take into account full specification of semver spec
* take into account prefix in tag of compare url
* fix compare url
* Git asking for username and email conf
* TypeError in CI because of PosixPath
* Handle issue pattern with one group [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Handle empty repository [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Catch missing remote [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)

#### Others

* Release of version 0.5.0
* (poetry): Update dependencies in lock file
* Fix Readme contributing description
* Add support for python3.8 [#51](https://gitlab.com/KeNaCo/auto-changelog/issues/51)
* Add integration tests for --tag-prefix --tag-pattern
* add more tests to test --compare-url option
* refactor assert condition to make it simpler
* add tests of --tag-prefix, --tag-pattern and --compare-url options
* Add --issue-pattern with invalid pattern integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --starting-commit with only one commit integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add skipping unreleased integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --stopping-commit integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --starting-commit integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --stdout integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --issue-pattern integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --issue-url integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --unreleased integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --latest-version integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --upstream integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --output integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --description integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --title integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --repo integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add --help integration test [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)
* Add integration tests [#50](https://gitlab.com/KeNaCo/auto-changelog/issues/50)

Full set of changes: [`0.4.0...0.5.0`](https://gitlab.com/KeNaCo/auto-changelog/compare/0.4.0...0.5.0)

## 0.4.0 (2019-10-31)

#### New Features

* (template): add release date to template

#### Fixes

* Missing {id} key in default issue template [#42](https://gitlab.com/KeNaCo/auto-changelog/issues/42)
* Git Repo now search in parent directories [#44](https://gitlab.com/KeNaCo/auto-changelog/issues/44)
* Missing release date in tests [#43](https://gitlab.com/KeNaCo/auto-changelog/issues/43)
* add support of ssh configuration of the remote
* fix generation of issue url
* clean old changes

#### Refactorings

* Remove unused import from test [#43](https://gitlab.com/KeNaCo/auto-changelog/issues/43)

#### Others

* Release of version 0.4.0
* (black): Black reformatting [#43](https://gitlab.com/KeNaCo/auto-changelog/issues/43)
* add tests to test new generation of issue url

Full set of changes: [`0.3.0...0.4.0`](https://gitlab.com/KeNaCo/auto-changelog/compare/0.3.0...0.4.0)

## 0.3.0 (2019-10-05)

#### New Features

* add --remote, --issue-url, --issue-pattern options, markdown links
* Latest version [#19](https://gitlab.com/KeNaCo/auto-changelog/issues/19)
* add --starting-commit option
* add --description option
* add --title option
* add --repo option
* add --stopping-commit option
* Unreleased option implemented [#19](https://gitlab.com/KeNaCo/auto-changelog/issues/19)
* Stdout option implemented [#19](https://gitlab.com/KeNaCo/auto-changelog/issues/19)
* Output option implemented [#19](https://gitlab.com/KeNaCo/auto-changelog/issues/19)
* Replace docopt with click [#19](https://gitlab.com/KeNaCo/auto-changelog/issues/19)
* New composing/parsing algorithm

#### Fixes

* Re-fix last fix in template and tests [#40](https://gitlab.com/KeNaCo/auto-changelog/issues/40)
* Missing empty space at the end of sections
* Remote url transformation cover all protocols ssh,git,http,https
* fix how to get url from remote
* add missing parameters
* Use all change types in template [#24](https://gitlab.com/KeNaCo/auto-changelog/issues/24)
* disable file writing when stdout specified
* fix latest_version
* fix crash on commit message with unsupported type

#### Refactorings

* Remove unused modules and files [#17](https://gitlab.com/KeNaCo/auto-changelog/issues/17)
* Typo in repository class name

#### Docs

* (Readme): Add gif with usage example [#21](https://gitlab.com/KeNaCo/auto-changelog/issues/21)
* (Readme): Update Readme [#21](https://gitlab.com/KeNaCo/auto-changelog/issues/21)

#### Others

* Release 0.3.0
* (ci): Add build and release jobs [#21](https://gitlab.com/KeNaCo/auto-changelog/issues/21)
* Update pyproject.toml [#21](https://gitlab.com/KeNaCo/auto-changelog/issues/21)
* Add black for formatting
* Remove docs and examples
* (poetry): Upgrade dependencies [#27](https://gitlab.com/KeNaCo/auto-changelog/issues/27)
* Use Poetry as dependency and build managing tool [#18](https://gitlab.com/KeNaCo/auto-changelog/issues/18)
* Set version to 1.0.0dev1 [#17](https://gitlab.com/KeNaCo/auto-changelog/issues/17)
* (git): Replace manual gitignore with new generated one [#17](https://gitlab.com/KeNaCo/auto-changelog/issues/17)
* (CI): Add gitlab CI support
* Reformatted by black
* Typo in docstrings
* Typo in test name
* Add pytest as testing framework

Full set of changes: [`0.1.7...0.3.0`](https://gitlab.com/KeNaCo/auto-changelog/compare/0.1.7...0.3.0)

## 0.1.7 (2017-11-18)

Full set of changes: [`0.1.6...0.1.7`](https://gitlab.com/KeNaCo/auto-changelog/compare/0.1.6...0.1.7)

## 0.1.6 (2017-08-09)

#### Fixes

* (template): fix tag date format

#### Docs

* Removed a space so the images are displayed correctly
* (README): Added example images to show what the script will do

Full set of changes: [`0.1.5...0.1.6`](https://gitlab.com/KeNaCo/auto-changelog/compare/0.1.5...0.1.6)

## 0.1.5 (2016-07-20)

#### Fixes

* Fixed IndexError when run with no tags in the repo [[#2](https://gitlab.com/KeNaCo/auto-changelog/issues/2)]

#### Others

* Bumped version number
* Bumping versions and trying to make PyPI installs see the template dir

Full set of changes: [`0.1.3...0.1.5`](https://gitlab.com/KeNaCo/auto-changelog/compare/0.1.3...0.1.5)

## 0.1.3 (2016-07-20)

#### Others

* Bumping version numbers to make pypi install properly

Full set of changes: [`0.1.2...0.1.3`](https://gitlab.com/KeNaCo/auto-changelog/compare/0.1.2...0.1.3)

## 0.1.2 (2016-07-20)

#### New Features

* Fixed setup.py so the templates are installed in the right spot
* Added an intermediate step to remove unnecessary newlines from the changelog

#### Fixes

* Fixed the issue of missing commits [[#1](https://gitlab.com/KeNaCo/auto-changelog/issues/1)]

#### Docs

* (examples): Updated the examples with cz-cli's changelog

#### Others

* Added a requirements.txt
* Updated changelog

Full set of changes: [`0.1.1...0.1.2`](https://gitlab.com/KeNaCo/auto-changelog/compare/0.1.1...0.1.2)

## 0.1.1 (2016-07-20)

#### New Features

* (template): Added "feature" group to changelog template
* Added a console script entry point, `auto-changelog`

#### Refactorings

* (templates): Refactored the templates to use a print_group() macro instead of manual copy/paste

#### Others

* Bumped the version number
* Added a changelog and makefile

Full set of changes: [`0.1.0...0.1.1`](https://gitlab.com/KeNaCo/auto-changelog/compare/0.1.0...0.1.1)

## 0.1.0 (2016-07-20)

#### New Features

* Wrote the setup.py file
* Converted from a jupyter notebook to a proper package

#### Docs

* (README): Added more detailed instructions to the README
* Added a README

#### Others

* Removed the Jupyter notebook stuff
* Removed the **pycache** crap that snuck in
