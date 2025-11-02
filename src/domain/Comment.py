from dataclasses import dataclass
from datetime import datetime

from domain.User import User


@dataclass(frozen=True)
class Comment(object):
    user: User
    url: str
    updated_at: datetime

    def __str__(self) -> str:
        return f"Comment(updated_at={self.updated_at}, user={self.user}, url={self.url})"
