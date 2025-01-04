from exeptions import (
    CandidateLevelError,
    DescriptionError,
    GitHubDomainError,
)
import re


def candidate_level_is_valid(level: str) -> bool:
    if not level:
        raise CandidateLevelError(message="Level must be not empty!")

    if type(level) is not str:
        raise CandidateLevelError(message=f"Type of level is {type(level)} but must be str!")

    if level not in["Junior", "Middle", "Senior"]:
        raise CandidateLevelError(
            message=f"The candidate's level must be equal to one of: Junior, Middle, Senior but was {level}!"
        )

    return True


def assignment_description_is_valid(description: str) -> bool:
    pattern = r"^[a-zA-Z\[\],.!?\(\)@#%:;\"']+$"

    if not description:
        raise DescriptionError(message="Description must be not empty!")

    if not bool(re.match(pattern, description)):
        raise DescriptionError(
            message="The text contains invalid characters! Use only latin a-z A-Z, and next symbols: [],.!?()@#%:;\"'"
        )

    if len(description) > 2500:
        raise DescriptionError(message="Max length of description must be 2500 symbols")

    return True


def git_url_is_valid(url: str) -> bool:
    base_url = "https://github.com/"

    if not url:
        raise GitHubDomainError(message="url must be not empty!")

    if not url.startswith(base_url):
        raise GitHubDomainError(message=f"url must start with {base_url}")

    return True



if __name__ == "__main__":
    pass
