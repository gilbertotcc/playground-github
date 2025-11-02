from dataclasses import dataclass

NON_HUMAN_USERS = ["dependabot", "github-actions"]

@dataclass(frozen=True)
class User(object):
    login_name: str

    def is_human(self) -> bool:
        return not self.login_name in NON_HUMAN_USERS
