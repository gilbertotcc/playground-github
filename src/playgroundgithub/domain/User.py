from dataclasses import dataclass

NON_HUMAN_USERS = ["dependabot", "github-actions"]

@dataclass(frozen=True)
class User:
    login_name: str

    def is_human(self) -> bool:
        return self.login_name not in NON_HUMAN_USERS
