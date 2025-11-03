from dataclasses import dataclass

from github import Auth, Github
from github.PullRequestComment import PullRequestComment

from playgroundgithub.domain.Comment import Comment
from playgroundgithub.domain.PullRequestUrl import PullRequestUrl
from playgroundgithub.domain.User import User


@dataclass(frozen=True)
class Configuration:
    github_pat: str


class GitHubClient:
    client: Github

    def __init__(self, client: Github):
        self.client = client

    def get_pr_comments(self, pull_request: PullRequestUrl) -> list[Comment]:
        def to_comment(pr_comment: PullRequestComment) -> Comment:
            return Comment(
                user=User(pr_comment.user.login),
                url=pr_comment.html_url,
                updated_at=pr_comment.updated_at
            )

        comments = (self.client
                    .get_repo(f"{pull_request.owner}/{pull_request.repository}")
                    .get_pull(pull_request.number)
                    .get_review_comments())
        return [to_comment(comment) for comment in comments]

    def close(self) -> None:
        self.client.close()


def create_github_client(configuration: Configuration) -> GitHubClient:
    auth_token = Auth.Token(configuration.github_pat)
    client = Github(auth=auth_token)
    return GitHubClient(client)
