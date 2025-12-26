import os
from dataclasses import dataclass

from dotenv import load_dotenv
from github import Auth, Github
from github.PullRequest import PullRequest as GitHubPullRequest  # noqa: TC002

from playgroundgithub.client.mapping import raw_comment_to_comment, raw_issue_to_pull_request
from playgroundgithub.domain import (
    PullRequest,
    PullRequestComment,
    PullRequestUrl,
    User,
)


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
        return self._to_pull_request(raw_pull_request, url)

    def get_pull_request_comments_of(
            self,
            pull_request: PullRequest
    ) -> list[PullRequestComment]:
        """
        Gets the comments of a pull request.

        The method returns both issue and review comments in an unified format.

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

    @staticmethod
    def _to_pull_request(
        pull_request: GitHubPullRequest, pull_request_url: PullRequestUrl
    ) -> PullRequest:
        return PullRequest(
            url=pull_request_url,
            title=pull_request.title,
            author=User(name=pull_request.user.login, type=pull_request.user.type),
            created_at=pull_request.created_at,
        )


def create_github_client(configuration: Configuration) -> GitHubClient:
    """
    Creates a GitHub client.

    :param configuration: The configuration for the client.
    :return: The GitHub client.
    """
    auth_token = Auth.Token(configuration.github_pat)
    client = Github(auth=auth_token)
    return GitHubClient(client)
