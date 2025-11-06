from dataclasses import dataclass, field

from playgroundgithub.domain.PullRequest import PullRequest
from playgroundgithub.domain.PullRequestComment import PullRequestComment
from playgroundgithub.domain.User import User


@dataclass
class PullRequestAnalysis:
    pull_request: PullRequest
    human_comment_counts: dict[User, int] = field(default_factory=dict)

    def add_comment(self, comment: PullRequestComment) -> None:
        if comment.user.type == "User":  # Add only comments made by humans
            self.human_comment_counts[comment.user] = (
                self.human_comment_counts.get(comment.user, 0) + 1
            )
