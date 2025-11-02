from dataclasses import dataclass
from github import Github, Auth
from github.PullRequestComment import PullRequestComment

from domain.Comment import Comment
from domain.user import User


@dataclass(frozen=True)
class Configuration(object):
    github_pat: str


class GitHubClient(object):
    client: Github

    def __init__(self, client: Github):
        self.client = client

    @staticmethod
    def create(configuration: Configuration) -> GitHubClient:
        auth_token = Auth.Token(configuration.github_pat)
        client = Github(auth=auth_token)
        return GitHubClient(client)

    def get_pr_comments(self, owner: str, repository: str, pr_number: int) -> list[Comment]:
        def to_pull_request_comment(pull_request_comment: PullRequestComment) -> Comment:
            return Comment(
                user=User(pull_request_comment.user.login),
                url=pull_request_comment.url,
                created_at=pull_request_comment.created_at
            )

        comments = self.client.get_repo(f"{owner}/{repository}").get_pull(pr_number).get_review_comments()
        return [to_pull_request_comment(comment) for comment in comments]

    def close(self):
        self.client.close()
