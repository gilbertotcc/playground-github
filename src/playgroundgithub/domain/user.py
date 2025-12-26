from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class User:
    name: str
    type: Literal["User"] | str
