import os

from dotenv import load_dotenv

from playgroundgithub.client.GitHubClient import Configuration, create_github_client
from playgroundgithub.domain.PullRequestUrl import pull_request_from_url
from playgroundgithub.service.PullRequestAnalyzer import PullRequestAnalyzer

load_dotenv()

def main() -> None:
    configuration = Configuration(os.getenv("GITHUB_TOKEN") or "")
    client = create_github_client(configuration)
    analyzer = PullRequestAnalyzer(client)

    pull_request_url = pull_request_from_url("https://github.com/totmoney/docs-parser/pull/2")

    metrics = analyzer.analyze_pull_request(pull_request_url)

    print(f"Metrics for pull request: {metrics.pull_request.title}")
    print(f"Author: {metrics.pull_request.author.login_name}")
    print("Participant comment counts:")
    for user, count in metrics.participant_comments_count.items():
        print(f"  - {user.login_name}: {count}")

    client.close()

if __name__ == "__main__":
    main()
