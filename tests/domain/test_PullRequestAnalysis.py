from datetime import datetime

from playgroundgithub.domain.PullRequest import PullRequest
from playgroundgithub.domain.PullRequestAnalysis import PullRequestAnalysis
from playgroundgithub.domain.PullRequestComment import PullRequestComment
from playgroundgithub.domain.PullRequestUrl import pull_request_from_url
from playgroundgithub.domain.User import User


class TestPullRequestAnalysis:
    def test_add_comment_should_succeed(self) -> None:
        pull_request_url = pull_request_from_url("https://github.com/owner/repo/pull/1")
        pull_request = PullRequest(
            url=pull_request_url,
            title="Test Title",
            author=User("author"),
            created_at=datetime.now(),
        )
        metrics = PullRequestAnalysis(pull_request=pull_request)
        comment = PullRequestComment(
            User("commenter"),
            "https://github.com/owner/repo/pull/1#issuecomment-1", datetime.now()
        )

        metrics.add_comment(comment)

        assert metrics.user_comment_counts[User("commenter")] == 1
