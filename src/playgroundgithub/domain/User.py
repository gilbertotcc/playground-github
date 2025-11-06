from dataclasses import dataclass

NON_HUMAN_USERS = ["dependabot", "github-actions"]

@dataclass(frozen=True)
class User:
    name: str

    def is_human(self) -> bool:
        return self.name in NON_HUMAN_USERS
