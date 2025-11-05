from dataclasses import dataclass

from github import Auth, Github
from github.IssueComment import IssueComment as GithubIssueComment
from github.PullRequest import PullRequest as GithubPullRequest
from github.PullRequestComment import PullRequestComment as GithubPullRequestComment

from playgroundgithub.domain.PullRequest import PullRequest
from playgroundgithub.domain.PullRequestComment import PullRequestComment
from playgroundgithub.domain.PullRequestUrl import PullRequestUrl
from playgroundgithub.domain.User import User


@dataclass(frozen=True)
class Configuration:
    """
    Configuration for the GitHub client.
    """
    github_pat: str


class GitHubClient:
    """
    A client for interacting with the GitHub API.
    """
    client: Github

    def __init__(self, client: Github):
        self.client = client

    def get_pr(self, pull_request_url: PullRequestUrl) -> PullRequest:
        """
        Gets a pull request.

        :param pull_request_url: The URL of the pull request.
        :return: The pull request.
        """
        pull_request = self._get_pull_request(pull_request_url)
        return self._to_pull_request(pull_request, pull_request_url)

    def get_pr_comments(
        self, pull_request_url: PullRequestUrl
    ) -> list[PullRequestComment]:
        """
        Gets the comments of a pull request.

        :param pull_request_url: The URL of the pull request.
        :return: The comments of the pull request.
        """
        pull_request = self._get_pull_request(pull_request_url)
        review_comments = pull_request.get_review_comments()

        issue = self.client.get_repo(
            f"{pull_request_url.owner}/{pull_request_url.repository}"
        ).get_issue(pull_request_url.number)
        issue_comments = issue.get_comments()

        comments = [self._to_comment(comment) for comment in review_comments]
        comments.extend([self._to_comment(comment) for comment in issue_comments])

        return comments

    def close(self) -> None:
        """
        Closes the client.
        """
        self.client.close()

    def _get_pull_request(self, pull_request_url: PullRequestUrl) -> GithubPullRequest:
        return self.client.get_repo(
            f"{pull_request_url.owner}/{pull_request_url.repository}"
        ).get_pull(pull_request_url.number)

    @staticmethod
    def _to_pull_request(
        pull_request: GithubPullRequest, pull_request_url: PullRequestUrl
    ) -> PullRequest:
        return PullRequest(
            url=pull_request_url,
            title=pull_request.title,
            author=User(pull_request.user.login),
            created_at=pull_request.created_at,
        )

    @staticmethod
    def _to_comment(
        pr_comment: GithubPullRequestComment | GithubIssueComment
    ) -> PullRequestComment:
        return PullRequestComment(
            user=User(pr_comment.user.login),
            url=pr_comment.html_url,
            updated_at=pr_comment.updated_at,
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
