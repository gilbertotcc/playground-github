from dataclasses import dataclass

from playgroundgithub.client.GitHubClient import GitHubClient
from playgroundgithub.domain.PullRequestMetrics import PullRequestMetrics
from playgroundgithub.domain.PullRequestUrl import PullRequestUrl


@dataclass
class PullRequestAnalyzer:
    github_client: GitHubClient
  
    def analyze_pull_request(
            self, pull_request_url: PullRequestUrl
        ) -> PullRequestMetrics:

        pull_request = self.github_client.get_pr(pull_request_url)
        metrics = PullRequestMetrics(pull_request=pull_request)

        comments = self.github_client.get_pr_comments(pull_request_url)
        for comment in comments:
            metrics = metrics.add_comment(comment)

        return metrics