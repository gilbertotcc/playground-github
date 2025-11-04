from datetime import datetime

from playgroundgithub.domain.PullRequest import PullRequest
from playgroundgithub.domain.PullRequestComment import PullRequestComment
from playgroundgithub.domain.PullRequestMetrics import PullRequestMetrics
from playgroundgithub.domain.PullRequestUrl import pull_request_from_url
from playgroundgithub.domain.User import User


class TestPullRequestMetrics:
    def test_add_comment_should_succeed(self) -> None:
        pull_request_url = pull_request_from_url("https://github.com/owner/repo/pull/1")
        pull_request = PullRequest(
            url=pull_request_url,
            title="Test Title",
            author=User("author"),
            created_at=datetime.now(),
        )
        metrics = PullRequestMetrics(pull_request=pull_request)
        comment = PullRequestComment(
            User("commenter"),
            "https://github.com/owner/repo/pull/1#issuecomment-1", datetime.now()
        )

        new_metrics = metrics.add_comment(comment)

        assert new_metrics is not metrics
        assert new_metrics.participant_comments_count[User("commenter")] == 1
