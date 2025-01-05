def url_extractor(url: str) -> tuple[str, str]:
    """Extract name of account and name of repository and return it in tuple"""

    res = url.split("/")
    repo = res[-1].split(".")[0]
    account = res[-2]
    return account, repo


def is_valid_file(file_name):
    """check is a file has a valid format"""
    valid_extensions = [".py", ".md", ".txt", ".rst", ".yml", ".json"]
    return any(file_name.endswith(ext) for ext in valid_extensions)