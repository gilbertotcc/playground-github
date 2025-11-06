import re
from dataclasses import dataclass, field

PR_URL_TEMPLATE = re.compile(r"^https://github.com/([^/]+)/([^/]+)/pull/([0-9]+)$")


@dataclass(frozen=True)
class PullRequestUrl:
    url: str
    _match: re.Match[str] = field(init=False, repr=False, hash=False, compare=False)

    def __post_init__(self) -> None:
        match = PR_URL_TEMPLATE.match(self.url)
        if match is None:
            raise ValueError(f"Invalid pull request URL {self.url}")
        object.__setattr__(self, "_match", match)

    @property
    def owner(self) -> str:
        return self._match.group(1)

    @property
    def repository(self) -> str:
        return self._match.group(2)

    @property
    def number(self) -> int:
        return int(self._match.group(3))


def pull_request_from_url(url: str) -> PullRequestUrl:
    return PullRequestUrl(url)
