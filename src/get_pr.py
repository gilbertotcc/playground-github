
from dotenv import load_dotenv

from playgroundgithub.client.client import Configuration, create_github_client
from playgroundgithub.domain import PullRequestUrl


load_dotenv()

def main() -> None:
    client = create_github_client(Configuration.load())
    pull_request_url = PullRequestUrl("https://github.com/totmoney/docs-parser/pull/2")

    pull_request = client.get_pull_request_from(pull_request_url)
    print(
        f"Found pull request: {pull_request.title} by {pull_request.author}"
    )
    print(f"URL: {pull_request.url.url}")
    print(f"Created at: {pull_request.created_at}")

    client.close()

if __name__ == "__main__":
    main()
