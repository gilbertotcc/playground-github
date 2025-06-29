# GitHub playground

## Development

The project uses [Ariadne Code Generator](https://github.com/mirumee/ariadne-codegen) to create the
GitHub GraphQL client.

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

## Resources

* <https://docs.github.com/public/fpt/schema.docs.graphql>
