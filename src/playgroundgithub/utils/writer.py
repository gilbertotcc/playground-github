import csv
import io
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from playgroundgithub.domain import PullRequestAnalysis, User


def csv_report_of(pull_request_analysis: list[PullRequestAnalysis]) -> str:
    unique_participants: set[User] = set()
    for pr_analysis in pull_request_analysis:
        unique_participants.update(pr_analysis.human_comment_counts.keys())

    sorted_participants = sorted(unique_participants, key=lambda u: u.name)

    header = [
        "Pull Request URL",
        "Title",
        "Author",
        "Created At",
        "Comments Count",
    ] + [user.name for user in sorted_participants]

    rows = [header]
    for pr_analysis in pull_request_analysis:
        comments_count = sum(pr_analysis.human_comment_counts.values())
        row = [
            str(pr_analysis.pull_request.url.url),
            str(pr_analysis.pull_request.title),
            str(pr_analysis.pull_request.author.name),
            str(pr_analysis.pull_request.created_at),
            str(comments_count),
        ]
        row.extend(
            [
                str(pr_analysis.human_comment_counts.get(participant, 0))
                for participant in sorted_participants
            ]
        )
        rows.append(row)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(rows)

    return output.getvalue()
