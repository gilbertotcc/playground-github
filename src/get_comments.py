import json
import os

from dotenv import load_dotenv

from client.GitHubClient import Configuration, GitHubClient
from domain.PullRequest import PullRequest

load_dotenv()


def main() -> None:
    configuration = Configuration(os.getenv("GITHUB_TOKEN") or "")
    client = GitHubClient.create(configuration)

    pull_request = PullRequest.from_url("https://github.com/totmoney/docs-parser/pull/2")

    comments = client.get_pr_comments(pull_request)
    counter = 0
    for comment in comments:
        counter += 1
        print(f"{counter}: Found comment {comment.url} by {comment.user.login_name}")

    client.close()

if __name__ == "__main__":
    main()