from typing import TYPE_CHECKING

from playgroundgithub.domain import PullRequestComment, User


if TYPE_CHECKING:
    from github.IssueComment import IssueComment as GitHubIssueComment
    from github.PullRequestComment import PullRequestComment as GitHubPullRequestComment


def raw_comment_to_comment(
        raw_comment: GitHubPullRequestComment | GitHubIssueComment
) -> PullRequestComment:
    user = User(name=raw_comment.user.login, type=raw_comment.user.type)
    return PullRequestComment(user=user,
                              url=raw_comment.html_url,
                              updated_at=raw_comment.updated_at)
