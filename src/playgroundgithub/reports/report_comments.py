import csv
import dataclasses
import io
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from playgroundgithub.client import GitHubClient
    from playgroundgithub.domain import PullRequest, PullRequestComment, User


@dataclasses.dataclass
class PullRequestComments:
    pull_request: PullRequest
    comment_counts: dict[User, int]

    @classmethod
    def of_pull_request(cls, pull_request: PullRequest) -> PullRequestComments:
        return cls(pull_request, {})

    def add_comment(self, comment: PullRequestComment) -> None:
        self.comment_counts[comment.user] = self.comment_counts.get(comment.user, 0) + 1


@dataclasses.dataclass
class CommentsReport:
    pull_request_comments_list: list[PullRequestComments]

    def to_csv(self) -> str:
        # Get all the unique commenters
        unique_commenters: set[User] = set()
        for pull_request_comments in self.pull_request_comments_list:
            for commenter in pull_request_comments.comment_counts:
                unique_commenters.add(commenter)
        sorted_unique_commenters = sorted(unique_commenters,
                                          key=lambda user: user.name)

        # Define CSV header row
        csv_header: list[str] = ["pull_request_url", "title", "author", "created_at"]
        csv_header.extend([commenter.name for commenter in sorted_unique_commenters])

        csv_rows: list[list[str]] = [csv_header]

        # Add CSV rows
        for pull_request_comments in self.pull_request_comments_list:
            csv_row: list[str] = [
                pull_request_comments.pull_request.url.url,
                pull_request_comments.pull_request.title,
                pull_request_comments.pull_request.author.name,
                str(pull_request_comments.pull_request.created_at) # Default
            ]
            csv_row.extend([
                str(pull_request_comments.comment_counts.get(commenter, 0))
                for commenter in sorted_unique_commenters
            ])
            csv_rows.append(csv_row)

        # Create the CSV
        string_output = io.StringIO()
        writer = csv.writer(string_output)
        writer.writerows(csv_rows)
        return string_output.getvalue()


@dataclasses.dataclass
class CommentsReportCreator:
    github_client: GitHubClient

    def create_comments_report(self, pull_requests: list[PullRequest]) -> CommentsReport:
        pull_request_comments_list: list[PullRequestComments] = []
        for pull_request in pull_requests:
            comments = self.github_client.get_pull_request_comments_of(pull_request)
            pull_request_comments = PullRequestComments.of_pull_request(pull_request)
            for comment in comments:
                if comment.user.type == "User":
                    pull_request_comments.add_comment(comment)

            pull_request_comments_list.append(pull_request_comments)

        return CommentsReport(pull_request_comments_list)

