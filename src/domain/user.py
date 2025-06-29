from dataclasses import dataclass

@dataclass(frozen=True)
class User(object):
    login_name: str
