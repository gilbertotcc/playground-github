import os

from dotenv import load_dotenv

from playgroundgithub.client.GitHubClient import Configuration, create_github_client
from playgroundgithub.service.PullRequestAnalyzer import PullRequestAnalyzer
from playgroundgithub.utils.reader import load_pull_requests_from_file
from playgroundgithub.utils.writer import csv_repport_of

load_dotenv()


def main() -> None:
    configuration = Configuration(os.getenv("GITHUB_TOKEN") or "")
    client = create_github_client(configuration)

    pull_request_urls = load_pull_requests_from_file("develop/prs.txt")

    analyzer = PullRequestAnalyzer(client)
    metrics = analyzer.analyze_pull_requests(pull_request_urls)

    report = csv_repport_of(metrics)

    print(report)

    client.close()


if __name__ == "__main__":
    main()
