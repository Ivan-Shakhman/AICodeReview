import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from repo_extractor import download_all_branches
from openai_worker import analyze_repo


client = TestClient(app)

@pytest.fixture
def mock_download_all_branches(mocker):
    return mocker.patch("repo_extractor.download_all_branches", return_value=None)


@pytest.fixture
def mock_analyze_repo(mocker):
    return mocker.patch("openai_worker.analyze_repo", return_value="Test response")


def test_title_screen():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to code review endpoint!" in response.json()["message"]


from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@patch("openai_worker.OpenAI")
@patch("repo_extractor.download_all_branches", return_value=None)
@patch("requests.get")
def test_make_code_review_success(mock_requests, mock_download_all_branches, mock_openai):
    mock_openai_instance = mock_openai.return_value
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
    mock_openai_instance.chat.completions.create.return_value = mock_response

    mock_requests.return_value = MagicMock(status_code=200, json=lambda: [{"name": "main"}])

    review_data = {
        "assignment_description": "Test project description",
        "git_repo_url": "https://github.com/user/repo.git",
        "open_api_key": "fake_api_key",
        "candidate_level": "Junior"
    }

    response = client.post("/", json=review_data)

    assert response.status_code == 200
    assert "Review" in response.json()
    assert response.json()["Review"] == "Test response"

    mock_openai_instance.chat.completions.create.assert_called_once()


def test_make_code_review_invalid_data():
    review_data = {
        "assignment_description": "",
        "git_repo_url": "invalid_url",
        "open_api_key": "fake_api_key",
        "candidate_level": "Junior"
    }

    response = client.post("/", json=review_data)

    assert response.status_code == 400


def test_make_code_review_invalid_level(mock_download_all_branches, mock_analyze_repo):
    review_data = {
        "assignment_description": "Test project description",
        "git_repo_url": "https://github.com/user/repo.git",
        "open_api_key": "fake_api_key",
        "candidate_level": "InvalidLevel"
    }

    response = client.post("/", json=review_data)

    assert response.status_code == 400
