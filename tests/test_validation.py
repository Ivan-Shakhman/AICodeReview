import pytest
from unittest.mock import patch
from exeptions import (
    CandidateLevelError,
    DescriptionError,
    GitHubDomainError,
)

from validators import (
    candidate_level_is_valid,
    assignment_description_is_valid,
    git_url_is_valid,
)


@pytest.mark.parametrize(
    "level, expected",
    [
        ("Junior", True),
        ("Middle", True),
        ("Senior", True),
        ("", False),
        (None, False),
        ("Invalid", False),
        (123, False),
    ],
)
def test_candidate_level_is_valid(level, expected):
    if expected:
        assert candidate_level_is_valid(level) is True
    else:
        with pytest.raises(CandidateLevelError):
            candidate_level_is_valid(level)


@pytest.mark.parametrize(
    "description, expected",
    [
        ("Valid description", True),
        ("Valid description with special chars!?", True),
        ("", False),
        (None, False),
        ("This description contains an invalid character like #.", False),
        ("a" * 2501, False),
    ],
)
def test_assignment_description_is_valid(description, expected):
    if expected:
        assert assignment_description_is_valid(description) is True
    else:
        with pytest.raises(DescriptionError):
            assignment_description_is_valid(description)


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://github.com/username/repository.git", True),
        ("https://github.com/username/repository", False),
        ("https://github.com/username/repository.git", True),
        ("", False),
        ("invalid_url", False),
    ],
)
def test_git_url_is_valid(url, expected):
    if expected:
        assert git_url_is_valid(url) is True
    else:
        with pytest.raises(GitHubDomainError):
            git_url_is_valid(url)


@patch("validators.logger")
def test_candidate_level_logging(mock_logger):
    level = "Junior"
    candidate_level_is_valid(level)
    mock_logger.info.assert_called_with("Validate level of candidate")

    level = "Invalid"
    with pytest.raises(CandidateLevelError):
        candidate_level_is_valid(level)
    mock_logger.error.assert_called_with(
        f"The candidate's level must be equal to one of: Junior, Middle, Senior but was {level}!"
    )
