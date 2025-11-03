from dataclasses import dataclass
from datetime import datetime

from playgroundgithub.domain.Comment import Comment
from playgroundgithub.domain.PullRequestUrl import PullRequestUrl
from playgroundgithub.domain.User import User


@dataclass
class PullRequestSummary:
    url: PullRequestUrl
    title: str
    author: User
    participant_comments_count: dict[User, int] | None
    created_at: datetime

    def add_comment(self, comment: Comment) -> None:
        if self.participant_comments_count is None:
            self.participant_comments_count = { comment.user: 1 }

        comments_count = self.participant_comments_count.get(comment.user, 0)
        self.participant_comments_count[comment.user] = comments_count + 1

def create_pull_request_summary(url: PullRequestUrl,
                                title: str,
                                author: User,
                                created_at: datetime
                                ) -> PullRequestSummary:
    return PullRequestSummary(url, title, author, {}, created_at)