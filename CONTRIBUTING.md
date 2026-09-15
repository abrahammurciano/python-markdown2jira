# uv

This project uses uv to manage dependencies. To get your development environment set up, run:

```sh
$ uv venv
```

The activate your shell environment by running:

```sh
$ source .venv/bin/activate
```

All future commands assume you have already run that in the current shell.

# Tests

This project uses pytest to run tests. To run tests locally, run:

```sh
$ pytest
```

Tests will be triggered in GitHub by opening a pull request to main.

# Documentation

Documentaion is generated using pdoc3. To generate documentation, run:

```sh
$ pdoc markdown2jira --html -o docs/ -f -c show_source_code=False
```

If you don't, it will be generated automatically on merge to main.

# Code style

Code is formatted and linted with ruff. Please keep it that way.

```sh
$ ruff format .
$ ruff check --fix .
```

If you don't format it, it will be formatted automatically on merge to main.

# Type checking

Code is type checked with mypy and basedpyright. Both are run in CI on every pull request.

```sh
$ mypy markdown2jira
$ basedpyright
```

# Deployment

To deploy a new version simply create a release on GitHub. The version will be automatically detected from the tag name. It should start with `v` and be followed by the actual version string.

Versions are deployed to PyPI automatically.
