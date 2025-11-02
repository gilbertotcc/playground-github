from dataclasses import dataclass
from datetime import datetime

from domain.user import User


@dataclass(frozen=True)
class Comment(object):
    user: User
    url: str
    created_at: datetime
