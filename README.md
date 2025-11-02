# GitHub playground

## Setup

The project uses [uv](https://docs.astral.sh/uv/) as the package manager to
simplify virtual environment setup, package management, and development.

To install the required packages, run the following command:

```sh
uv sync
```

### Gemini CLI

This project uses Gemini CLI.
To enable its features, configure the following environment variables and save
them in a `.env` file.

* `GITHUB_TOKEN`: GitHub Personal Access Token required for the GitHub MCP server.
  See [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
  for token creation instructions.
* `CONTEXT7_API_KEY`: Context7 API key.
  See [Context7](https://github.com/upstash/context7).

## Run

TODO

## Development

To work on the code, you must also add development dependencies.
Run:

```sh
uv sync —dev
```

To add new dependencies, use the following command:

```sh
uv add <dependeny>
```

The project uses
[Ariadne Code Generator](https://github.com/mirumee/ariadne-codegen) to create
the GitHub GraphQL client.

To create it, you must run:

```shell
pipenv run generate-graphql-client
```

The resulting files will be placed in the directory `src/client/graphql`.

## Limitations

* The analysis of the PRs has these limitations:
  * Max contributors: 10
  * Max comments: 50
  * Max review threads: 50
  * Max comments per review thread: 50

## Bruno collection

This project provides a [Bruno](https://www.usebruno.com/) collection in the
folder `bruno` for working with the GitHub API.
It allows you to test API operations during Python development.

Before using this collection, create your own GitHub Personal Access Token and
save it in a `.env` file in the `bruno/GitHub` directory.
The `.env.example` file in the repository provides a template with a sample
value.

For more information on creating a token, please refer to the official
documentation on
[Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

## Resources

* <https://docs.github.com/public/fpt/schema.docs.graphql>
