import os
from unittest.mock import patch, mock_open
import base64
from utils import url_extractor
from repo_extractor import (
    get_all_branches,
    download_branch_content,
    save_branch_content,
    download_file,
    download_all_branches
)


@patch("requests.get")
def test_get_all_branches(mock_get):
    mock_get.return_value.json.return_value = [{"name": "main"}, {"name": "dev"}]
    branches = get_all_branches("user", "repo")
    assert branches == ["main", "dev"]


@patch("requests.get")
def test_download_branch_content(mock_get):
    mock_get.return_value.json.return_value = [{"type": "file", "name": "file1.txt", "content": "base64content"}]
    content = download_branch_content("main", "user", "repo")
    assert content[0]["name"] == "file1.txt"


@patch("requests.get")
@patch("builtins.open", new_callable=mock_open)
def test_download_file(mock_open, mock_get):
    mock_get.return_value.content = b"file content"
    download_file("https://example.com/file", "downloaded_repo/file")
    mock_open.assert_called_once_with("downloaded_repo/file", "wb")
    mock_open.return_value.write.assert_called_once_with(b"file content")


@patch("builtins.open", new_callable=mock_open)
def test_save_branch_content(mock_open):
    content = [{"type": "file", "name": "file1.txt", "content": base64.b64encode(b"some content").decode()}]
    save_branch_content("main", content)
    mock_open.assert_called_once_with(os.path.normpath("downloaded_repo/main/file1.txt"), "wb")
    mock_open.return_value.write.assert_called_once()


@patch("repo_extractor.get_all_branches")
@patch("repo_extractor.download_branch_content")
@patch("repo_extractor.save_branch_content")
def test_download_all_branches(mock_save, mock_download, mock_get):
    mock_get.return_value = ["main", "dev"]
    mock_download.return_value = [{"type": "file", "name": "file1.txt", "content": "base64content"}]
    download_all_branches("https://github.com/user/repo")
    mock_get.assert_called_once()
    mock_download.assert_called()
    mock_save.assert_called()


@patch("repo_extractor.url_extractor")
def test_url_extractor(mock_extractor):
    mock_extractor.return_value = ("user", "repo")
    owner, repo = url_extractor("https://github.com/user/repo")
    assert owner == "user"
    assert repo == "repo"
