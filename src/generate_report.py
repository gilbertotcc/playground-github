
from dotenv import load_dotenv

from playgroundgithub.client import GitHubClient
from playgroundgithub.client.client import Configuration
from playgroundgithub.service.pull_request_analyzer import PullRequestAnalyzer
from playgroundgithub.utils.reader import load_pull_requests_from_file
from playgroundgithub.utils.writer import csv_report_of


load_dotenv()


def main() -> None:
    client = GitHubClient.new_client(Configuration.load())

    pull_request_urls = load_pull_requests_from_file("develop/prs.txt")

    analyzer = PullRequestAnalyzer(client)
    metrics = analyzer.analyze_pull_requests(pull_request_urls)

    report = csv_report_of(metrics)

    print(report)

    client.close()


if __name__ == "__main__":
    main()
