#!/usr/bin/env python3

import click
from datetime import datetime, UTC
import json

from client.list_repositories import list_repositories
from client.list_pull_requests_with_comments import list_pull_requests_with_comments


@click.command()
@click.option("--org", required=True, help="GitHub organisation login name")
@click.option("--from-date", required=True, help="From date (ISO8601, e.g. 2025-06-01")
@click.option("--to-date", required=True, help="To date (ISO8601, e.g. 2025-06-30)")
def main(org, from_date, to_date):
    from_date = datetime.fromisoformat(from_date).replace(tzinfo=UTC)
    to_date = datetime.fromisoformat(to_date).replace(tzinfo=UTC)

    repos = list_repositories(organization=org, updated_from=from_date, updated_to=to_date)
    print(f"Found {len(repos)} changed repositories")

    prs = [
        list_pull_requests_with_comments(repo, from_date, to_date)
        for repo in repos
    ]

    print(json.dumps(prs, default=lambda x: x.__dict__,indent=2))

    # for repo in repos:
    #     result = list_pull_requests_with_comments(repo.organization, repo.name, from_date, to_date)
    #     print(json.dumps(result, default=lambda x: x.__dict__,indent=2))

if __name__ == "__main__":
    main()
