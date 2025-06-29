#!/usr/bin/env python3

import click
from datetime import datetime, UTC
import json

from dotenv import load_dotenv
import os

import asyncio

from client.GitHubClient import GitHubClient, Configuration
#from client.list_repositories import list_repositories
from client.list_pull_requests_with_comments import list_pull_requests_with_comments

load_dotenv()

@click.command()
@click.option("--org", required=True, help="GitHub organisation login name")
@click.option("--from-date", required=True, help="From date (ISO8601, e.g. 2025-06-01")
@click.option("--to-date", required=True, help="To date (ISO8601, e.g. 2025-06-30)")
def main(org, from_date, to_date):
    async def async_main(org, from_date, to_date):
        from_date = datetime.fromisoformat(from_date).replace(tzinfo=UTC)
        to_date = datetime.fromisoformat(to_date).replace(tzinfo=UTC)

        github_client_configuration = Configuration(
            github_token=os.getenv("GITHUB_TOKEN")
        )
        github_client = GitHubClient.new_client(github_client_configuration)

        repos = await github_client.list_updated_repositories(organization=org,
                                                        from_date=from_date,
                                                        to_date=to_date)

    #    repos = list_repositories(organization=org, updated_from=from_date, updated_to=to_date)
        print(f"Found {len(repos)} changed repositories")

        prs = [
            list_pull_requests_with_comments(repo, from_date, to_date)
            for repo in repos
        ]

        print(json.dumps(prs, default=lambda x: x.__dict__,indent=2))

        # for repo in repos:
        #     result = list_pull_requests_with_comments(repo.organization, repo.name, from_date, to_date)
        #     print(json.dumps(result, default=lambda x: x.__dict__,indent=2))
    asyncio.run(async_main(org, from_date, to_date))

if __name__ == "__main__":
    main()
