
from dotenv import load_dotenv

from playgroundgithub.client import GitHubClient
from playgroundgithub.client.client import Configuration
from playgroundgithub.reports.report_comments import CommentsReportCreator
from playgroundgithub.utils.logging import setup_logging
from playgroundgithub.utils.reader import load_pull_requests_from_file


load_dotenv()


def main() -> None:
    client = GitHubClient.new_client(Configuration.load())

    pull_request_urls = load_pull_requests_from_file("develop/prs.txt")
    pull_requests = [client.get_pull_request_from(url) for url in pull_request_urls]

    report = CommentsReportCreator(client).create_comments_report(pull_requests)

    print(report.to_csv())

    client.close()


if __name__ == "__main__":
    setup_logging()
    main()
