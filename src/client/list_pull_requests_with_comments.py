from datetime import datetime, UTC
from functools import reduce
from itertools import groupby, chain
from typing import List

import requests
from dotenv import load_dotenv
import os
import sys

from domain.pullrequest import ParticipantComments, PullRequest
from domain.repository import Repository
from domain.user import User

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

PRS_WITH_COMMENTS_QUERY = """
query ClosedOrMergedPullRequestsWithReviewComments(
  $owner: String!
  $name: String!
  $afterPr: String
) {
  repository(owner: $owner, name: $name) {
    name
    pullRequests(
      first: 50
      after: $afterPr
      baseRefName: "develop"
      states: [CLOSED, MERGED]
      orderBy: { field: UPDATED_AT, direction: DESC }
    ) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        number
        title
        body
        url
        headRefName
        author {
          login
        }
        participants(first: 10) {
          nodes {
            login
          }
        }
        createdAt
        mergedAt
        closedAt
        comments(first: 50) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            author {
              login
            }
            createdAt
            updatedAt
            body
            url
          }
        }
        reviewThreads(first: 50) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            comments(first: 50) {
              nodes {
                author {
                  login
                }
                createdAt
                updatedAt
                body
                url
              }
            }
          }
        }
      }
    }
  }
}
"""


def parse_comments(comments_json) -> List[ParticipantComments]:
    return list(map(
        lambda comment_json: ParticipantComments(
            participant=comment_json["author"]["login"],
            comments_count=1
        ),
        comments_json
    ))


def parse_pr_comments(pr_comments_json) -> List[ParticipantComments]:
    return parse_comments(pr_comments_json)


def parse_thread_comments(thread_comments_json) -> List[ParticipantComments]:
    return parse_comments(thread_comments_json)


def parse_participants(participants_json) -> List[User]:
    return list(map(
        lambda participant: User(participant["login"]),
        participants_json
    ))


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


def list_pull_requests_with_comments(
    repository: Repository,
    from_date: datetime,
    to_date: datetime
):
    pull_requests = []
    after_pr = None

    keep_going = True

    while keep_going:
        vars = {
            "owner": repository.organization,
            "name": repository.name,
            "afterPr": after_pr
        }

        data = run_query(PRS_WITH_COMMENTS_QUERY, vars)
        pr_nodes = data["data"]["repository"]["pullRequests"]["nodes"]
        page_info = data["data"]["repository"]["pullRequests"]["pageInfo"]

        for pr in pr_nodes:
            # ⏫ Get closedAt or mergedAt
            closed_at = pr["closedAt"]
            merged_at = pr["mergedAt"]

            pr_date_str = closed_at or merged_at
            if not pr_date_str:
                continue  # skip weird dangling PRs

            pr_date = datetime.fromisoformat(pr_date_str).replace(tzinfo=UTC)

            if pr_date < from_date:
                # ⏹️ Older than window: stop looping!
                keep_going = False
                break

            if from_date <= pr_date <= to_date:

                participants = parse_participants(pr["participants"]["nodes"])

                pr_comments = parse_comments(pr["comments"]["nodes"])

                review_comments_list = list(map(
                    lambda thread: parse_thread_comments(thread["comments"]["nodes"]),
                    pr["reviewThreads"]["nodes"]
                ))
                review_comments = list(chain.from_iterable(review_comments_list))

                participants_comments = list(chain(
                    pr_comments, review_comments
                ))

                total_comments_count = len(participants_comments)

                comments_by_participant = groupby(
                    sorted(participants_comments,
                           key=lambda comment: comment.participant),
                    lambda comment: comment.participant
                )

                total_comments_by_participant = [reduce(
                    lambda accumulator, comment: ParticipantComments(
                        participant=accumulator.participant,
                        comments_count=accumulator.comments_count + comment.comments_count
                    ),
                    group
                ) for _, group in comments_by_participant
                ]

                pull_request = PullRequest(
                    repository=repository, # FIXME: Add value
                    number= pr["number"],
                    title=pr["title"],
                    body=pr["body"],
                    url=pr["url"],
                    author=User(pr["author"]["login"]),
                    participants=participants,
                    total_comments_count=total_comments_count,
                    participants_comments=total_comments_by_participant
                )

                pull_requests.append(pull_request)

        if keep_going and page_info["hasNextPage"]:
            after_pr = page_info["endCursor"]
        else:
            break

    return pull_requests
