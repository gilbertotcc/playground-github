from playgroundgithub.domain.PullRequestUrl import PullRequestUrl, pull_request_from_url


def load_pull_requests_from_file(file_path: str) -> list[PullRequestUrl]:
    with open(file_path) as file:
        urls = [pull_request_from_url(line.strip()) for line in file if line.strip()]
    return urls
