from dataclasses import dataclass
from datetime import datetime
from typing import List

from client.graphql import Client, OrganisationRepositoriesOrganizationRepositoriesNodes, \
    ClosedOrMergedPullRequestsWithReviewCommentsRepositoryPullRequestsNodes
from domain.pullrequest import PullRequest
from domain.repository import Repository


def repository_from_node(
        organization: str,
        node: OrganisationRepositoriesOrganizationRepositoriesNodes) -> Repository:
    return Repository(organization=organization, name=node.name)


def pull_request_from_node(
        node: ClosedOrMergedPullRequestsWithReviewCommentsRepositoryPullRequestsNodes,
        repository: Repository
) -> PullRequest:
    author = 

    return PullRequest(
        repository=repository,
        number=node.number,
        title=node.title,
        body=node.body,
        author=
    )


@dataclass
class Configuration(object):
    github_token: str

@dataclass
class GitHubClient(object):
    graphql_client: Client

    async def list_updated_repositories(self,
                                        organization: str,
                                        from_date: datetime,
                                        to_date: datetime) -> List[Repository]:

        repositories: List[Repository] = []
        cursor = None

        while True:
            raw_result = await self.graphql_client.organisation_repositories(
                org=organization, after_repo=cursor
            )

            nodes = raw_result.organization.repositories.nodes
            page_info = raw_result.organization.repositories.page_info

            for node in nodes:
                updated_at = datetime.fromisoformat(node.updated_at)
                if from_date <= updated_at <= to_date:
                    repository = repository_from_node(organization, node)
                    repositories.append(repository)
                elif updated_at < from_date:
                    return repositories

            if page_info.has_next_page and page_info.end_cursor:
                cursor = page_info.end_cursor
            else:
                break

        return repositories



    async def list_pull_requests(self,
                                 repository: Repository,
                                 from_date: datetime,
                                 to_date: datetime)\
            -> List[PullRequest]:

        pull_requests = []
        cursor = None

        while True:
            raw_result = await self.graphql_client.closed_or_merged_pull_requests_with_review_comments(
                owner=repository.organization,
                name=repository.name
            )

            nodes = raw_result.repository.pull_requests.nodes
            page_info = raw_result.repository.pull_requests.page_info

            for node in nodes:
                updated_at = datetime.fromisoformat(node.updated_at)
                if from_date <= updated_at <= to_date:
                    repository =
                    repositories.append(repository)
                elif updated_at < from_date:
                    return repositories

            if page_info.has_next_page and page_info.end_cursor:
                cursor = page_info.end_cursor
            else:
                break

        return pull_requests


    @staticmethod
    def new_client(configuration: Configuration) -> "GitHubClient":
        graphql_client = Client(
            url="https://api.github.com/graphql",
            headers={
                "Authorization": f"Bearer {configuration.github_token}"
            }
        )
        return GitHubClient(graphql_client)
