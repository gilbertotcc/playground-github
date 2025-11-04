import re
from dataclasses import dataclass, field

PR_URL_TEMPLATE = re.compile(r"^https://github.com/([^/]+)/([^/]+)/pull/([0-9]+)$")

@dataclass(frozen=True)
class PullRequestUrl:
    url: str
    owner: str = field(repr=False)
    repository: str = field(repr=False)
    number: int = field(repr=False)

def pull_request_from_url(url: str) -> PullRequestUrl:
    match = PR_URL_TEMPLATE.match(url)
    if match is None:
        raise ValueError(f"Invalid pull request URL {url}")

    owner, repository, number = match.group(1, 2, 3)
    return PullRequestUrl(url, owner, repository, number=int(number))
