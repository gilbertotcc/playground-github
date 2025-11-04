from dataclasses import dataclass, field

from playgroundgithub.domain.PullRequest import PullRequest
from playgroundgithub.domain.PullRequestComment import PullRequestComment
from playgroundgithub.domain.User import User


@dataclass(frozen=True)
class PullRequestMetrics:
    pull_request: PullRequest
    participant_comments_count: dict[User, int] = field(default_factory=dict)

    def add_comment(self, comment: PullRequestComment) -> "PullRequestMetrics":
        new_comments_count = self.participant_comments_count.copy()
        new_comments_count[comment.user] = self.participant_comments_count\
            .get(comment.user, 0) + 1
        return PullRequestMetrics(
            pull_request=self.pull_request,
            participant_comments_count=new_comments_count,
        )
