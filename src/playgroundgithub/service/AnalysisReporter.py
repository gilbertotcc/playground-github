import csv
import io

from playgroundgithub.domain.PullRequestMetrics import PullRequestMetrics
from playgroundgithub.domain.User import User


class AnalysisReporter:

    def create_report(self, pull_request_metrics: list[PullRequestMetrics]) -> str:
        unique_participants: set[User] = set()
        for pr_metrics in pull_request_metrics:
            unique_participants.update(pr_metrics.participant_comments_count.keys())

        sorted_participants = sorted(
            list(unique_participants), key=lambda u: u.login_name
        )

        header = [
            "Pull Request URL",
            "Title",
            "Author",
            "Created At",
            "Comments Count",
        ] + [user.login_name for user in sorted_participants]

        rows = [header]
        for pr_metrics in pull_request_metrics:
            comments_count = sum(pr_metrics.participant_comments_count.values())
            row = [
                str(pr_metrics.pull_request.url.url),
                str(pr_metrics.pull_request.title),
                str(pr_metrics.pull_request.author.login_name),
                str(pr_metrics.pull_request.created_at),
                str(comments_count),
            ]
            row.extend([
                str(pr_metrics.participant_comments_count.get(participant, 0))
                for participant in sorted_participants
            ])
            rows.append(row)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(rows)

        return output.getvalue()
