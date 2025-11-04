# Gemini Code Assistant Context

This document provides context for the Gemini code assistant to understand the
project and provide better assistance.

## Project Overview

This is a Python project that interacts with the GitHub API using the `PyGithub`
library.
The main functionality is to fetch pull request comments and summarize pull
request information.

The project is structured into two main parts:

* **`src/get_comments.py`**: An example script that demonstrates how to use the
  `GitHubClient` to fetch comments for a pull request.
* **`src/playgroundgithub`**: The main application package, containing the
  following modules:
  * **`client`**: Contains the `GitHubClient` for interacting with the GitHub
    API.
  * **`domain`**: Defines the data models for the application, such as
    `Comment`, `PullRequestUrl`, `PullRequestSummary`, and `User`.

## Building and Running

The project uses `uv` for package management.

To install dependencies:

```sh
uv sync
```

To run the example script:

```sh
python src/get_comments.py
```

## Development Conventions

The project uses f-strings for string formatting and type hints for static
analysis.
Domain models are implemented as dataclasses.

After making any changes, please run the quality checks to ensure the code is
correct and follows the project's style guide.

## Quality Checks

To run the tests use:

```sh
uv run pytest
```

To verify code quality use the following commands:

```sh
uv run mypy
uv run ruff check
```

To check Markdown files quality, run this command:

```sh
markdownlint-cli2 <filename>
```

You can also use `--fix` parameter to let the linter to fix fixable errors.

```sh
markdownlint-cli2 --fix <filename>
```

## Project Architecture

The project follows a simple architecture:

* **Domain Objects**: The `domain` package contains plain old Python objects
  (POPOs) that represent the application's data models. These objects are
  immutable (where appropriate) and have no knowledge of how they are persisted
  or retrieved.
* **Client**: The `client` package contains the `GitHubClient`, which is
  responsible for interacting with the GitHub API. It takes domain objects as
  input and returns domain objects as output. This separation of concerns
  makes the application easier to test and maintain.
* **Scripts**: The `src` directory contains scripts that use the `client` and
  `domain` packages to implement the application's functionality.
