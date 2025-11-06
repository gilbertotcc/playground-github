from dataclasses import dataclass

from playgroundgithub.client.GitHubClient import GitHubClient
from playgroundgithub.domain.PullRequestAnalysis import PullRequestAnalysis
from playgroundgithub.domain.PullRequestUrl import PullRequestUrl


@dataclass
class PullRequestAnalyzer:
    github_client: GitHubClient

    def analyze_pull_requests(
            self, pull_request_urls: list[PullRequestUrl]
        ) -> list[PullRequestAnalysis]:
        
        all_analysis = []
        for pull_request_url in pull_request_urls:
            pr_analysis = self.analyze_pull_request(pull_request_url)
            all_analysis.append(pr_analysis)

        return all_analysis
  
    def analyze_pull_request(
            self, pull_request_url: PullRequestUrl
        ) -> PullRequestAnalysis:

        pull_request = self.github_client.get_pr(pull_request_url)
        analysis = PullRequestAnalysis(pull_request=pull_request)

        comments = self.github_client.get_pr_comments(pull_request_url)
        for comment in comments:
            analysis.add_comment(comment)

        return analysis
