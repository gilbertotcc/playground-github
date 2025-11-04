import os

from dotenv import load_dotenv

from playgroundgithub.client.GitHubClient import Configuration, create_github_client
from playgroundgithub.domain.PullRequestUrl import pull_request_from_url

load_dotenv()

def main() -> None:
    configuration = Configuration(os.getenv("GITHUB_TOKEN") or "")
    client = create_github_client(configuration)
    pull_request_url = pull_request_from_url("https://github.com/totmoney/docs-parser/pull/2")

    pull_request = client.get_pr(pull_request_url)
    print(
        f"Found pull request: {pull_request.title} by {pull_request.author.login_name}"
    )
    print(f"URL: {pull_request.url.url}")
    print(f"Created at: {pull_request.created_at}")

    client.close()

if __name__ == "__main__":
    main()
