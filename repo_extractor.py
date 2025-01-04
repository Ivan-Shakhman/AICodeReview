import base64
import os
import json
import requests
from dotenv import load_dotenv


load_dotenv()
OWNER = "Ivan-Shakhman"
REPO = "Theatre-API-Service"
URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/"
BRANCHES_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/branches"
BRANCH = "develop"
GIT_KEY = os.getenv("GitHubAPIKey")
HEADER = {"Authorization": f"Bearer {GIT_KEY}"}
response = requests.get(URL, headers=HEADER)
branch_response = requests.get(BRANCHES_URL, headers=HEADER)
if response.status_code == 200:
    print(response.content)


trees = []
if branch_response.status_code == 200:
    response_json = json.loads(branch_response.content)

    for value in response_json:
        trees.append(value["name"])
    print(trees)


def get_branch_sha():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/branches/{BRANCH}"
    response = requests.get(url, headers=HEADER)
    response.raise_for_status()
    return response.json()["commit"]["sha"]


def get_tree(sha):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{sha}?recursive=1"
    response = requests.get(url, headers=HEADER)
    response.raise_for_status()
    return response.json()["tree"]


def download_file(file_path, file_url):
    response = requests.get(file_url)
    response.raise_for_status()
    data = response.json()

    file_content = base64.b64decode(data["content"])

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as file:
        file.write(file_content)


def main():
    backup_dir = "backup"
    os.makedirs(backup_dir, exist_ok=True)

    branch_sha = get_branch_sha()
    tree = get_tree(branch_sha)
    for item in tree:
        if item["type"] == "blob":
            file_path = os.path.join(backup_dir, item["path"])
            print(f"Downloading {file_path}...")
            download_file(file_path, item["url"])


if __name__ == "__main__":
    main()
