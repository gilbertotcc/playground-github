from dataclasses import dataclass, field
from datetime import datetime

from playgroundgithub.domain.Comment import Comment
from playgroundgithub.domain.PullRequestUrl import PullRequestUrl
from playgroundgithub.domain.User import User


@dataclass(frozen=True)
class PullRequestSummary:
    url: PullRequestUrl
    title: str
    author: User
    created_at: datetime
    participant_comments_count: dict[User, int] = field(default_factory=dict)

    def add_comment(self, comment: Comment) -> "PullRequestSummary":
        new_comments_count = self.participant_comments_count.copy()
        new_comments_count[comment.user] = self.participant_comments_count\
            .get(comment.user, 0) + 1
        return PullRequestSummary(
            url=self.url,
            title=self.title,
            author=self.author,
            created_at=self.created_at,
            participant_comments_count=new_comments_count,
        )
