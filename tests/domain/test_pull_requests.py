import pytest

from playgroundgithub.domain import PullRequestUrl


def test_pull_request_url_should_succeed() -> None:
    url = "https://github.com/gilbertotcc/playground-bluetooth/pull/1"

    pull_request_url = PullRequestUrl(url)

    assert pull_request_url.owner == "gilbertotcc"
    assert pull_request_url.repository == "playground-bluetooth"
    assert pull_request_url.number == 1

def test_pull_request_url_should_fail() -> None:
    url = "https://github.com/..."

    with pytest.raises(ValueError) as exception_info:
        PullRequestUrl(url)

    assert "Invalid pull request URL " in str(exception_info.value)
