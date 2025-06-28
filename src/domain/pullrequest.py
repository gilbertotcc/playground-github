from dataclasses import dataclass
from typing import List

from domain.user import User
from domain.repository import Repository


@dataclass(frozen=True)
class ParticipantComments(object):
    participant: User
    comments_count: int


@dataclass(frozen=True)
class PullRequest(object):
    repository: Repository
    number: int
    title: str
    body: str
    url: str
    author: User
    participants: List[User]
    total_comments_count: int
    participants_comments: List[ParticipantComments]
