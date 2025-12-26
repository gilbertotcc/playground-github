from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from github import Auth, Github

from playgroundgithub.client.mapping import (
    raw_comment_to_comment,
    raw_issue_to_pull_request,
    raw_pull_request_to_pull_request,
)


if TYPE_CHECKING:
    from playgroundgithub.domain import PullRequest, PullRequestComment, PullRequestUrl


@dataclass(frozen=True)
class Configuration:
    """
    GitHub Personal Access Token (PAT)
    """
    github_pat: str

    @classmethod
    def load(cls) -> Configuration:
        load_dotenv()

        github_pat = os.getenv("GITHUB_TOKEN")

        if github_pat is None:
            raise RuntimeError("GITHUB_TOKEN environment variable not set")

        return cls(github_pat)



class GitHubClient:
    """
    A client for interacting with the GitHub API.
    """
    client: Github

    def __init__(self, client: Github):
        self.client = client

    @classmethod
    def new_client(cls, configuration: Configuration) -> GitHubClient:
        auth_token = Auth.Token(configuration.github_pat)
        client = Github(auth=auth_token)
        return cls(client)

    def search_pull_requests(self, query_string: str) -> list[PullRequest]:
        query = query_string if "is:pr" in query_string else f"{query_string} is:pr"
        raw_pull_requests = self.client.search_issues(query=query)

        return [raw_issue_to_pull_request(raw_pull_request) for raw_pull_request in raw_pull_requests]

    def get_pull_request_from(self, url: PullRequestUrl) -> PullRequest:
        """
        Gets a pull request.

        :param url: The URL of the pull request.
        :return: The pull request.
        """
        raw_pull_request = (self
                            .client.get_repo(f"{url.owner}/{url.repository}")
                            .get_pull(url.number))
        return raw_pull_request_to_pull_request(raw_pull_request)

    def get_pull_request_comments_of(
            self,
            pull_request: PullRequest
    ) -> list[PullRequestComment]:
        """
        Gets the comments of a pull request.

        The method returns both issue and review comments in a unified format.

        :param pull_request: The pull request.
        :return: The comments of the pull request.
        """
        raw_repository = self.client.get_repo(
            f"{pull_request.url.owner}/{pull_request.url.repository}"
        )

        raw_pull_request = raw_repository.get_pull(pull_request.url.number)
        raw_pull_reqeust_comments = raw_pull_request.get_review_comments()

        raw_issue_comments = (raw_repository
                              .get_issue(pull_request.url.number)
                              .get_comments())

        comments = [raw_comment_to_comment(comment) for comment in raw_pull_reqeust_comments]
        comments.extend([raw_comment_to_comment(comment) for comment in raw_issue_comments])

        return comments

    def close(self) -> None:
        self.client.close()
