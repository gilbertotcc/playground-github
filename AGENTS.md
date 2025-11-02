# Gemini Code Assistant Context

This document provides context for the Gemini code assistant to understand the
project and provide better assistance.

## Project Overview

This is a Python project that provides a command-line tool to interact with the
GitHub API.
It uses `click` for the command-line interface, `requests` for making HTTP
requests, and `ariadne-codegen` to generate a GraphQL client from a schema.

The main functionality is to list repositories and pull requests for a given
GitHub organization within a specified date range.

The project is structured into three main parts:

* **`src/list_repositories.py`**: The main entry point for the command-line
  tool.
* **`src/client`**: Contains the `GitHubClient` for interacting with the GitHub
  GraphQL API.
* **`src/domain`**: Defines the data models for the application, such as
  `Repository`, `PullRequest`, and `User`.

## Building and Running

The project uses `uv` for package management.

To install dependencies:

```sh
uv sync
```

To run the command-line tool:

```sh
python src/list_repositories.py --org <organization> --from-date <start-date> --to-date <end-date>
```

## Development Conventions

The project uses `ariadne-codegen` to generate the GraphQL client.
The configuration for this is in `pyproject.toml`.
To regenerate the client, run:

```sh
uv sync --dev
pipenv run generate-graphql-client
```

The generated client is located in `src/client/graphql`.

The project uses f-strings for string formatting and type hints for static
analysis.
