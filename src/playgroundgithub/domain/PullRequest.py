from dataclasses import dataclass
from datetime import datetime

from playgroundgithub.domain.PullRequestUrl import PullRequestUrl
from playgroundgithub.domain.User import User


@dataclass(frozen=True)
class PullRequest:
    url: PullRequestUrl
    title: str
    author: User
    created_at: datetime
