import os

from dotenv import load_dotenv

from playgroundgithub.client.GitHubClient import Configuration, create_github_client
from playgroundgithub.domain.PullRequestUrl import pull_request_from_url
from playgroundgithub.service.AnalysisReporter import AnalysisReporter
from playgroundgithub.service.PullRequestAnalyzer import PullRequestAnalyzer

load_dotenv()


def main() -> None:
    configuration = Configuration(os.getenv("GITHUB_TOKEN") or "")
    client = create_github_client(configuration)
    
    pull_request_urls = [
        pull_request_from_url("https://github.com/totmoney/onboarding/pull/1989"),
        pull_request_from_url("https://github.com/totmoney/docs-parser/pull/1"),
        pull_request_from_url("https://github.com/totmoney/transactions/pull/2099"),
    ]

    analyzer = PullRequestAnalyzer(client)
    metrics = analyzer.analyze_pull_requests(pull_request_urls)
    
    reporter = AnalysisReporter()
    report = reporter.create_report(metrics)
    
    print(report)

    client.close()


if __name__ == "__main__":
    main()
