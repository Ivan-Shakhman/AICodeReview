import base64
import os
import json
import requests
from dotenv import load_dotenv
from utils import url_extractor
import logging


logger = logging.getLogger("uvicorn")

load_dotenv()

GIT_KEY = os.getenv("GitHubAPIKey")
HEADER = {}
"""if you want to try download many times add your GIT_KEY to .env"""
if GIT_KEY:
    HEADER["Authorization"] = f"Bearer {GIT_KEY}"


def get_all_branches(owner: str, repo: str):
    """return list of branch names"""
    logger.info("Get all branches from repository")

    url = f"https://api.github.com/repos/{owner}/{repo}/branches"
    response = requests.get(url, headers=HEADER)

    if response.raise_for_status():
        logger.error(f"ERROR! {response.raise_for_status()}")

    logger.info("Success!")
    return [branch["name"] for branch in response.json()]


def download_branch_content(branch_name: str, owner: str, repo: str):
    logger.info(f"Downloading content of branch: {branch_name}")

    url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    params = {"ref": branch_name}
    response = requests.get(url, headers=HEADER, params=params)

    if response.raise_for_status():
        logger.error(f"ERROR! {response.raise_for_status()}")

    logger.info("Success.")
    return response.json()


def save_branch_content(branch_name, content, parent_dir=""):
    logger.info(f"Start downloading all files from branch {branch_name}")

    branch_dir = os.path.join("downloaded_repo", branch_name, parent_dir)
    os.makedirs(branch_dir, exist_ok=True)

    for item in content:
        if item["type"] == "blob" or item["type"] == "file":

            if "content" in item:
                file_path = os.path.join(branch_dir, item["name"])
                file_content = base64.b64decode(item["content"])
                with open(file_path, "wb") as f:
                    f.write(file_content)
                    logger.info(f"{item["name"]} downloaded successfully.")

            elif "download_url" in item:
                file_url = item["download_url"]
                file_path = os.path.join(branch_dir, item["name"])
                download_file(file_url, file_path)
                logger.info(f"{item["name"]} downloaded successfully.")

            else:
                logger.warning(f"Skipping item without 'content' or 'download_url' key: {item}")

        elif item["type"] == "dir":
            dir_content_url = item["url"]
            response = requests.get(dir_content_url, headers=HEADER)
            response.raise_for_status()
            dir_content = response.json()
            save_branch_content(branch_name, dir_content, os.path.join(parent_dir, item["name"]))
            logger.info(f"{item["name"]} downloaded successfully.")
        else:
            logger.warning(f"Skipping unsupported item type: {item['type']}")


def download_file(url, save_path):
    logger.info("start downloading file...")

    try:
        response = requests.get(url, headers=HEADER)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        logger.info(f"Success. Downloaded file saved to {save_path}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading {url}: {e}")


def download_all_branches(url: str):
    owner, repo = url_extractor(url)
    branches = get_all_branches(owner=owner, repo=repo)

    for branch in branches:

        try:
            content = download_branch_content(branch, owner, repo)
            save_branch_content(branch, content)

        except Exception as e:
            logger.error(f"ERROR: {e}")
