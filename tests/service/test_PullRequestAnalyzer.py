from datetime import datetime
from unittest.mock import MagicMock

from playgroundgithub.domain.PullRequest import PullRequest
from playgroundgithub.domain.PullRequestComment import PullRequestComment
from playgroundgithub.domain.PullRequestUrl import PullRequestUrl, pull_request_from_url
from playgroundgithub.domain.User import User
from playgroundgithub.service.PullRequestAnalyzer import PullRequestAnalyzer


def create_pull_request_comment(user: str, url: str) -> PullRequestComment:
    return PullRequestComment(
        user=User(user),
        url=url,
        updated_at=datetime.now(),
    )

class TestPullRequestAnalyzer:
    def test_analyze_pull_request_should_succeed(self) -> None:
        # Arrange
        github_client = MagicMock()
        pull_request_url = pull_request_from_url("https://github.com/owner/repo/pull/1")

        pull_request = PullRequest(
            url=pull_request_url,
            title="Test Title",
            author=User("author"),
            created_at=datetime.now(),
        )
        github_client.get_pr.return_value = pull_request

        comments = [
            create_pull_request_comment("commenter1", "url1"),
            create_pull_request_comment("commenter2", "url2"),
            create_pull_request_comment("commenter1", "url3"),
        ]
        github_client.get_pr_comments.return_value = comments

        analyzer = PullRequestAnalyzer(github_client=github_client)

        # Act
        analysis = analyzer.analyze_pull_request(pull_request_url)

        # Assert
        github_client.get_pr.assert_called_once_with(pull_request_url)
        github_client.get_pr_comments.assert_called_once_with(pull_request_url)

        assert analysis.pull_request == pull_request
        assert len(analysis.user_comment_counts) == 2
        assert analysis.user_comment_counts[User("commenter1")] == 2
        assert analysis.user_comment_counts[User("commenter2")] == 1

    def test_analyze_pull_requests_should_succeed(self) -> None:
        # Arrange
        github_client = MagicMock()

        pr_url1 = pull_request_from_url("https://github.com/owner/repo/pull/1")
        pr1 = PullRequest(pr_url1, "PR 1", User("author1"), datetime.now())
        comments1 = [create_pull_request_comment("c1", "u1")]

        pr_url2 = pull_request_from_url("https://github.com/owner/repo/pull/2")
        pr2 = PullRequest(pr_url2, "PR 2", User("author2"), datetime.now())
        comments2 = [
            create_pull_request_comment("c2", "u2"),
            create_pull_request_comment("c2", "u3"),
        ]

        def get_pr_side_effect(pull_request_url: PullRequestUrl) -> PullRequest | None:
            if pull_request_url == pr_url1:
                return pr1
            if pull_request_url == pr_url2:
                return pr2
            return None

        def get_pr_comments_side_effect(
                pull_request_url: PullRequestUrl
            ) -> list[PullRequestComment]:
            
            if pull_request_url == pr_url1:
                return comments1
            if pull_request_url == pr_url2:
                return comments2
            return []

        github_client.get_pr.side_effect = get_pr_side_effect
        github_client.get_pr_comments.side_effect = get_pr_comments_side_effect

        analyzer = PullRequestAnalyzer(github_client=github_client)
        pull_request_urls = [pr_url1, pr_url2]

        # Act
        all_analysis = analyzer.analyze_pull_requests(pull_request_urls)

        # Assert
        assert len(all_analysis) == 2

        analysis1 = all_analysis[0]
        assert analysis1.pull_request == pr1
        assert sum(analysis1.user_comment_counts.values()) == 1
        assert analysis1.user_comment_counts[User("c1")] == 1

        analysis2 = all_analysis[1]
        assert analysis2.pull_request == pr2
        assert sum(analysis2.user_comment_counts.values()) == 2
        assert analysis2.user_comment_counts[User("c2")] == 2
