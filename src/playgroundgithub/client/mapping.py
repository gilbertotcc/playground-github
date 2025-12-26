from typing import TYPE_CHECKING

from playgroundgithub.domain import PullRequest, PullRequestComment, PullRequestUrl, User


if TYPE_CHECKING:
    from github.Issue import Issue as GitHubIssue
    from github.IssueComment import IssueComment as GitHubIssueComment
    from github.PullRequestComment import PullRequestComment as GitHubPullRequestComment


def raw_comment_to_comment(
        raw_comment: GitHubPullRequestComment | GitHubIssueComment
) -> PullRequestComment:
    user = User(name=raw_comment.user.login, type=raw_comment.user.type)
    return PullRequestComment(user=user,
                              url=raw_comment.html_url,
                              updated_at=raw_comment.updated_at)

def raw_issue_to_pull_request(raw_issue: GitHubIssue) -> PullRequest:
    url = PullRequestUrl(url=raw_issue.html_url)
    author = User(name=raw_issue.user.login, type=raw_issue.user.type)

    return PullRequest(url=url,
                       title=raw_issue.title,
                       author=author,
                       created_at=raw_issue.created_at)
