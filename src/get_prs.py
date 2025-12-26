
from dotenv import load_dotenv

from playgroundgithub.client.client import Configuration, create_github_client


load_dotenv()

def main() -> None:
    client = create_github_client(Configuration.load())

    query = ""  # TODO: Set the query

    pull_requests = client.search_pull_requests(query)
    for pull_request in pull_requests:
        print(f"{pull_request.url.url}")

    client.close()



if __name__ == "__main__":
    main()
