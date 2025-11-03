import os

from dotenv import load_dotenv

from client.GitHubClient import Configuration, create_github_client
from domain.PullRequest import pull_request_from_url

load_dotenv()


def main() -> None:
    configuration = Configuration(os.getenv("GITHUB_TOKEN") or "")
    client = create_github_client(configuration)

    pull_request = pull_request_from_url("https://github.com/totmoney/docs-parser/pull/2")

    comments = client.get_pr_comments(pull_request)
    counter: int = 0
    for comment in comments:
        counter = counter + 1
        print(f"{counter}: Found comment {comment.url} by {comment.user.login_name}")

    client.close()

if __name__ == "__main__":
    main()