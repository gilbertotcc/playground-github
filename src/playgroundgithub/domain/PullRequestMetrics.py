from dataclasses import dataclass, field

from playgroundgithub.domain.PullRequest import PullRequest
from playgroundgithub.domain.PullRequestComment import PullRequestComment
from playgroundgithub.domain.User import User


@dataclass
class PullRequestMetrics:
    pull_request: PullRequest
    participant_comments_count: dict[User, int] = field(default_factory=dict)

    def add_comment(self, comment: PullRequestComment) -> None:
        self.participant_comments_count[comment.user] = (
            self.participant_comments_count.get(comment.user, 0) + 1
        )
