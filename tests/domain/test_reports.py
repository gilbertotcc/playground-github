from datetime import datetime

from playgroundgithub.domain import PullRequest, PullRequestComment, PullRequestUrl, User
from playgroundgithub.domain.reports import PullRequestAnalysis


class TestPullRequestAnalysis:
    def test_add_comment_should_succeed(self) -> None:
        pull_request_url = PullRequestUrl("https://github.com/owner/repo/pull/1")
        pull_request = PullRequest(
            url=pull_request_url,
            title="Test Title",
            author=User("author", type="User"),
            created_at=datetime.now(),
        )
        metrics = PullRequestAnalysis(pull_request=pull_request)
        comment = PullRequestComment(
            User("commenter", type="User"),
            "https://github.com/owner/repo/pull/1#issuecomment-1", datetime.now()
        )

        metrics.add_comment(comment)

        assert metrics.human_comment_counts[User("commenter", type="User")] == 1
