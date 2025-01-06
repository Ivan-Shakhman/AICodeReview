import os
import pytest
from unittest.mock import MagicMock
from openai import OpenAI
from openai_worker import analyze_file, analyze_repo


@pytest.fixture
def mock_openai_client(mocker):
    mock_openai = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
    mock_openai.chat.completions.create.return_value = mock_response
    mocker.patch("openai_worker.OpenAI", return_value=mock_openai)
    return mock_openai


@pytest.fixture
def mock_is_valid_file(mocker):
    return mocker.patch("utils.is_valid_file", return_value=True)


@pytest.fixture
def mock_os_walk(mocker):
    mock_os_walk = mocker.patch("os.walk")
    mock_os_walk.return_value = [
        ("downloaded_repo", ["subdir"], ["file1.py", "file2.py", "invalid_file.txt"])
    ]
    return mock_os_walk


def test_analyze_file(mocker):
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="file content"))

    result = analyze_file("test_file.py")

    mock_open.assert_called_once_with("test_file.py", "r", encoding="utf-8-sig", errors="ignore")
    assert result == "file content"


def test_analyze_repo(mocker, mock_openai_client, mock_is_valid_file, mock_os_walk):
    result = analyze_repo(
        description="Test repo description",
        level="beginner",
        api_key="fake_api_key",
        repo_dir="downloaded_repo"
    )

    assert "Test response" in result
    mock_openai_client.chat.completions.create.assert_called_once()

