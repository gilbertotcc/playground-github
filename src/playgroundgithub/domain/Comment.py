from dataclasses import dataclass
from datetime import datetime

from playgroundgithub.domain.User import User


@dataclass(frozen=True)
class Comment:
    user: User
    url: str
    updated_at: datetime

    def __str__(self) -> str:
        return \
            f"Comment(updated_at={self.updated_at}, user={self.user}, url={self.url})"
