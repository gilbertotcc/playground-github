
from dotenv import load_dotenv

from playgroundgithub.client import GitHubClient
from playgroundgithub.client.client import Configuration
from playgroundgithub.domain import PullRequestUrl
from playgroundgithub.utils.logging import setup_logging


load_dotenv()


def main() -> None:
    client = GitHubClient.new_client(Configuration.load())
    pull_request = client.get_pull_request_from(
        PullRequestUrl("https://github.com/totmoney/docs-parser/pull/2")
    )

    comments = client.get_pull_request_comments_of(pull_request)
    counter: int = 0
    for comment in comments:
        counter = counter + 1
        print(f"{counter}: Found comment {comment.url} by {comment.user}")

    client.close()

if __name__ == "__main__":
    setup_logging()
    main()
