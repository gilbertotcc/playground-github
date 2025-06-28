from dataclasses import dataclass

@dataclass(frozen=True)
class Repository(object):
    organization: str
    name: str
