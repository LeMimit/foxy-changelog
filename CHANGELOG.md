# Foxy changelog

A tool which generates a changelog and manage version for any git repository using conventional style.

## 1.1.0

> `2024-01-21`

### New features 🚀

* **version**: add version management support ([#15](https://github.com/LeMimit/foxy-changelog/issues/15))

### Fixes 🐞

* **commit**: add missing import ([#16](https://github.com/LeMimit/foxy-changelog/issues/16))

### Continuous integration 🐹

* **python**: remove unused and not working workflow ([#17](https://github.com/LeMimit/foxy-changelog/issues/17))

Full set of changes: [`1.0.0...1.1.0`](https://github.com/LeMimit/foxy-changelog/compare/1.0.0...1.1.0)

## 1.0.0

> `2024-01-17`

### New features 🚀

* **commit**: support new types - deps, tools and version ([#6](https://github.com/LeMimit/foxy-changelog/issues/6))
* **template**: display dependency updates as table when possible ([#12](https://github.com/LeMimit/foxy-changelog/issues/12))
* **template**: sort scope in generated changelog ([#10](https://github.com/LeMimit/foxy-changelog/issues/10))
* **template**: improve default template ([#8](https://github.com/LeMimit/foxy-changelog/issues/8))

### Docs 📚

* **readme**: update readme with fork information ([#1](https://github.com/LeMimit/foxy-changelog/issues/1))
* **template**: add issue and pr templates ([#2](https://github.com/LeMimit/foxy-changelog/issues/2))

### Tools 🧰

* **hatch**: use hatch as build system ([#4](https://github.com/LeMimit/foxy-changelog/issues/4))

Full set of changes: [`0.6.0...1.0.0`](https://github.com/LeMimit/foxy-changelog/compare/0.6.0...1.0.0)

## 0.6.0

> `2022-11-27`

### New features 🚀

* add support gitlab
* add support of custom template (--template)
* Adding debug messages for commit parsing/changelog generation
* Add debug mode
* change how is managed compare_url feature
* add --tag-prefix, --tag-pattern and --compare-url options
* Add --tag-pattern option [#19](https://github.com/LeMimit/foxy-changelog/issues/19) (credit to @LeMimit)
* add --remote, --issue-url, --issue-pattern options, markdown links
* Latest version [#19](https://github.com/LeMimit/foxy-changelog/issues/19)
* add --starting-commit option
* add --description option
* add --title option
* add --repo option
* add --stopping-commit option
* Unreleased option implemented [#19](https://github.com/LeMimit/foxy-changelog/issues/19)
* Stdout option implemented [#19](https://github.com/LeMimit/foxy-changelog/issues/19)
* Output option implemented [#19](https://github.com/LeMimit/foxy-changelog/issues/19)
* Replace docopt with click [#19](https://github.com/LeMimit/foxy-changelog/issues/19)
* New composing/parsing algorithm
* Fixed setup.py so the templates are installed in the right spot
* Added an intermediate step to remove unnecessary newlines from the changelog
* Added a console script entry point, `auto-changelog`
* Wrote the setup.py file
* Converted from a jupyter notebook to a proper package
* **template**: add release date to template
* **template**: Added "feature" group to changelog template

### Fixes 🐞

* FIxes bug <https://github.com/KeNaCo/auto-changelog/issues/112>
* updated jinja2 / click deps
* default_issue_pattern
* change option from --repo to --path-repo
* sanitaztion of remote url
* Improve parsing of conventional commits by considering breaking changes
* Handling of multiline bodies and footer
* Missing link feature control for diffs [#74](https://github.com/LeMimit/foxy-changelog/issues/74)
* test_tag_pattern works for all py versions
* change compare_url to diff_url
* take into account full specification of semver spec
* take into account prefix in tag of compare url
* fix compare url
* Git asking for username and email conf
* TypeError in CI because of PosixPath
* Handle issue pattern with one group [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Handle empty repository [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Catch missing remote [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Missing {id} key in default issue template [#42](https://github.com/LeMimit/foxy-changelog/issues/42)
* Git Repo now search in parent directories [#44](https://github.com/LeMimit/foxy-changelog/issues/44)
* Missing release date in tests [#43](https://github.com/LeMimit/foxy-changelog/issues/43)
* add support of ssh configuration of the remote
* fix generation of issue url
* clean old changes
* Re-fix last fix in template and tests [#40](https://github.com/LeMimit/foxy-changelog/issues/40)
* Missing empty space at the end of sections
* Remote url transformation cover all protocols ssh,git,http,https
* fix how to get url from remote
* add missing parameters
* Use all change types in template [#24](https://github.com/LeMimit/foxy-changelog/issues/24)
* disable file writing when stdout specified
* fix latest_version
* fix crash on commit message with unsupported type
* Fixed IndexError when run with no tags in the repo [[#2](https://github.com/LeMimit/foxy-changelog/issues/2)]
* Fixed the issue of missing commits [[#1](https://github.com/LeMimit/foxy-changelog/issues/1)]
* **git**: clean references after process
* **regex**: accept empty additional commit body
* **template**: fix tag date format
* **tests**: Prevent GPG pass and sing issues
* **tests**: Failing double line test expects link

### Refactorings 🏭

* computation of remote url
* Remove unused import from test [#43](https://github.com/LeMimit/foxy-changelog/issues/43)
* Remove unused modules and files [#17](https://github.com/LeMimit/foxy-changelog/issues/17)
* Typo in repository class name
* **templates**: Refactored the templates to use a print_group() macro instead of manual copy/paste
* **tests**: Replace parcial asserts with full content comparison
* **tests**: Replace files with --allow-empty parameter for commit

### Tests 🧪

* add invalid template  finle name test
* Small improvements in multiple tests
* Add more tests for default remote
* Add notes from JS implementation cross testing
* add integration and unit testing
* refactor integration test
* remove xfail markers from integration tests
* Add integration tests for issue [#79](https://github.com/LeMimit/foxy-changelog/issues/79)
* Add integration tests for --tag-prefix --tag-pattern
* add more tests to test --compare-url option
* refactor assert condition to make it simpler
* add tests of --tag-prefix, --tag-pattern and --compare-url options
* Add --issue-pattern with invalid pattern integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --starting-commit with only one commit integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add skipping unreleased integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --stopping-commit integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --starting-commit integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --stdout integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --issue-pattern integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --issue-url integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --unreleased integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --latest-version integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --upstream integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --output integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --description integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --title integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --repo integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add --help integration test [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* Add integration tests [#50](https://github.com/LeMimit/foxy-changelog/issues/50)
* add tests to test new generation of issue url
* Add pytest as testing framework

### Docs 📚

* update readme
* Update "Contributing" section in README to cover usage of make and pre-commit
* Add usage section and command line options to README
* Removed a space so the images are displayed correctly
* Added a README
* **README**: Added example images to show what the script will do
* **README**: Added more detailed instructions to the README
* **Readme**: Add gif with usage example [#21](https://github.com/LeMimit/foxy-changelog/issues/21)
* **Readme**: Update Readme [#21](https://github.com/LeMimit/foxy-changelog/issues/21)
* **examples**: Updated the examples with cz-cli's changelog

### Others 🔨

* Add Makefile for build automation
* Add tox for local multi environment testing
* Add pre-commit and hooks for black and flake8
* Add flake8 as linter
* Add dependency to black for dev environment
* Release of version 0.6.0
* update requirements
* set up pre-commit in Gitlab CI
* set up tests in a GitHub actions
* set up pre-commit in a GitHub actions
* update tooling
* drop support for python 3.6
* Release of version 0.5.3
* Add sandbox folder to gitignore
* Release of version 0.5.1
* Release of version 0.5.0
* Fix Readme contributing description
* Add support for python3.8 [#51](https://github.com/LeMimit/foxy-changelog/issues/51)
* Release of version 0.4.0
* Release 0.3.0
* Update pyproject.toml [#21](https://github.com/LeMimit/foxy-changelog/issues/21)
* Add black for formatting
* Remove docs and examples
* Use Poetry as dependency and build managing tool [#18](https://github.com/LeMimit/foxy-changelog/issues/18)
* Set version to 1.0.0dev1 [#17](https://github.com/LeMimit/foxy-changelog/issues/17)
* Bumped version number
* Bumping versions and trying to make PyPI installs see the template dir
* Bumping version numbers to make pypi install properly
* Added a requirements.txt
* Updated changelog
* Bumped the version number
* Added a changelog and makefile
* Removed the Jupyter notebook stuff
* Removed the **pycache** crap that snuck in
* **CI**: Add gitlab CI support
* **ci**: Add build and release jobs [#21](https://github.com/LeMimit/foxy-changelog/issues/21)
* **flake8**: remove unused import
* **git**: Replace manual gitignore with new generated one [#17](https://github.com/LeMimit/foxy-changelog/issues/17)
* **poetry**: update locked dependencies
* **poetry**: update pyproject.toml to use poetry.groups
* **poetry**: Update dependencies in lock file
* **poetry**: Upgrade dependencies [#27](https://github.com/LeMimit/foxy-changelog/issues/27)
* **python**: drop python 3.5, add support for python 3.9
* black
* fix flakes complains
* Remove unused import
* Line-break long strings
* Use raw string for regex pattern
* Run black on previous PR
* Reformatted by black
* Typo in docstrings
* Typo in test name
* **black**: fix unsupported py39 target
* **black**: Black reformatting [#43](https://github.com/LeMimit/foxy-changelog/issues/43)
