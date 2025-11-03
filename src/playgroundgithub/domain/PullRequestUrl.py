import re
from dataclasses import dataclass

PR_URL_TEMPLATE = re.compile(r"^https://github.com/([^/]+)/([^/]+)/pull/([0-9]+)$")

@dataclass
class PullRequestUrl:
    url: str
    owner: str
    repository: str
    number: int

    def __init__(self, url: str, owner: str, repository: str, number: int):
        self.url = url
        self.owner = owner
        self.repository = repository
        self.number = number

    def __str__(self) -> str:
        return f"PullRequest(url={self.url})"


def pull_request_from_url(url: str) -> PullRequestUrl:
    match = PR_URL_TEMPLATE.match(url)
    if match is None:
        raise ValueError(f"Invalid pull request URL {url}")

    owner, repository, number = match.group(1, 2, 3)
    return PullRequestUrl(url, owner, repository, number=int(number))