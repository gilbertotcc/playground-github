from datetime import datetime

from playgroundgithub.domain.Comment import Comment
from playgroundgithub.domain.PullRequestSummary import PullRequestSummary
from playgroundgithub.domain.PullRequestUrl import PullRequestUrl
from playgroundgithub.domain.User import User


class TestPullRequestSummary:
    def test_add_comment_should_succeed(self) -> None:
        summary = PullRequestSummary(
            url=PullRequestUrl(
                "https://github.com/owner/repo/pull/1", "owner", "repo", 1),
            title="Test Title",
            author=User("author"),
            created_at=datetime.now(),
        )
        comment = Comment(
            User("commenter"),
            "https://github.com/owner/repo/pull/1#issuecomment-1", datetime.now())

        new_summary = summary.add_comment(comment)

        assert new_summary is not summary
        assert new_summary.participant_comments_count[User("commenter")] == 1
