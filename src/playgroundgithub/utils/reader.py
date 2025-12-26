from playgroundgithub.domain import PullRequestUrl


def load_pull_requests_from_file(file_path: str) -> list[PullRequestUrl]:
    with open(file_path) as file:
        urls = [PullRequestUrl.from_url(line.strip()) for line in file if line.strip()]
    return urls
