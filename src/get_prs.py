
import argparse

from dotenv import load_dotenv

from playgroundgithub.client import GitHubClient
from playgroundgithub.client.client import Configuration


load_dotenv()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="The query to search for pull requests.")
    args = parser.parse_args()

    client = GitHubClient.new_client(Configuration.load())

    pull_requests = client.search_pull_requests(args.query)
    for pull_request in pull_requests:
        print(f"{pull_request.url.url}")

    client.close()



if __name__ == "__main__":
    main()
