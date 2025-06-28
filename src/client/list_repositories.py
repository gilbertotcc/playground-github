from datetime import datetime
from typing import List

import requests
from dotenv import load_dotenv
import os
import sys

from domain.repository import Repository

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("❌ Missing GITHUB_TOKEN. Set it in your environment or in a `.env` file.")
    sys.exit(1)

GITHUB_API_URL = "https://api.github.com/graphql"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/json",
}

ORG_REPOS_QUERY = """
query OrganisationRepositories($org: String!, $afterRepo: String) {
  organization(login: $org) {
    repositories(
      first: 100
      after: $afterRepo
      isArchived: false
      orderBy: { field: UPDATED_AT, direction: DESC }
    ) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        name
        isPrivate
        createdAt
        updatedAt
      }
    }
  }
}
"""


def run_query(query, variables):
    response = requests.post(
        GITHUB_API_URL,
        headers=HEADERS,
        json={"query": query, "variables": variables},
        timeout=30,
    )
    if response.status_code != 200:
        print(f"❌ HTTP {response.status_code}: {response.text}")
        sys.exit(1)

    result = response.json()
    if "errors" in result:
        print(f"❌ GraphQL errors: {result['errors']}")
        sys.exit(1)
    return result


def list_repositories(organization: str, updated_from: datetime, updated_to: datetime) -> List[Repository]:
    repos: List[Repository] = []
    after = None

    while True:
        vars = {
            "org": organization,
            "afterRepo": after
        }

        data = run_query(ORG_REPOS_QUERY, vars)
        nodes = data["data"]["organization"]["repositories"]["nodes"]
        page_info = data["data"]["organization"]["repositories"]["pageInfo"]

        # TODO: Results are sorted by updatedAt, so the cycle can stop before
        for repo in nodes:
            updated_at = datetime.fromisoformat(repo["updatedAt"])
            if updated_from <= updated_at <= updated_to:
                repository: Repository = Repository(
                    organization=organization,
                    name=repo["name"]
                )
                repos.append(repository)

        if page_info["hasNextPage"]:
            after = page_info["endCursor"]
        else:
            break

    return repos
