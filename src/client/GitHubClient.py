from dataclasses import dataclass
from datetime import datetime
from typing import List

from client.graphql import Client, OrganisationRepositoriesOrganizationRepositoriesNodes
from domain.repository import Repository


def repository_from_node(
        organization: str,
        node: OrganisationRepositoriesOrganizationRepositoriesNodes) -> Repository:
    return Repository(organization=organization, name=node.name)


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



    def list_pull_requests(self):
        pass

    @staticmethod
    def new_client(configuration: Configuration) -> "GitHubClient":
        graphql_client = Client(
            url="https://api.github.com/graphql",
            headers={
                "Authorization": f"Bearer {configuration.github_token}"
            }
        )
        return GitHubClient(graphql_client)
