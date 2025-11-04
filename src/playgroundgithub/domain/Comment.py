from dataclasses import dataclass
from datetime import datetime

from playgroundgithub.domain.User import User


@dataclass(frozen=True)
class PullRequestComment:
    user: User
    url: str
    updated_at: datetime
