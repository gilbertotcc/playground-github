from playgroundgithub.domain.PullRequestUrl import PullRequestUrl

import pytest


class TestPullRequestUrl:

    def test_from_url_should_succeed(self) -> None:
        url = "https://github.com/gilbertotcc/playground-bluetooth/pull/1"

        pull_request_url = PullRequestUrl.from_url(url)

        assert pull_request_url.owner == "gilbertotcc"
        assert pull_request_url.repository == "playground-bluetooth"
        assert pull_request_url.number == 1

    def test_from_url_should_fail(self) -> None:
        url = "https://github.com/..."

        with pytest.raises(ValueError) as exception_info:
            PullRequestUrl.from_url(url)

        assert "Invalid pull request URL " in str(exception_info.value)
