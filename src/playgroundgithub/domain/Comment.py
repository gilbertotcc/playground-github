from dataclasses import dataclass
from datetime import datetime

from playgroundgithub.domain.User import User


@dataclass(frozen=True)
class Comment:
    user: User
    url: str
    updated_at: datetime
