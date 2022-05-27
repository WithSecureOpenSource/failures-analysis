# Contributing
Project uses poetry and invoke to setup development environment. See [Poetry](https://python-poetry.org/)
documentation how to install Poetry in your operating system. Then use `poetry install` to
install required dependencies.

Test can be run by: `poetry run invoke test
`
Bug fix or feature should be covered by tests and test(s) should be places in `utest` folder. Project uses
Python [pytest](https://docs.pytest.org) and is recommended to use plain functions in tests.

Commit messages should use [Angular style](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commits)
because project uses [Python semantic release](https://python-semantic-release.readthedocs.io/en/latest/index.html#)
package and commit message defines the next version number. More details about commit message format can be found from
[parsing commit logs](https://python-semantic-release.readthedocs.io/en/latest/commit-log-parsing.html#commit-log-parsing)

# Release 
Release is done automatically by a GitHub action. Release is triggered automatically with
[Python semantic release](https://python-semantic-release.readthedocs.io/en/latest/index.html#) and pushed out to PyPi

