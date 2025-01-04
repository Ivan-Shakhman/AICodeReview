from exeptions import CandidateLevelError, ValidCharactersError, LengthError, GitHubDomainError
import re


def candidate_level_is_valid(level: str) -> bool:
    if type(level) is not str:
        raise TypeError(f"Type of level is {type(level)} but must be str!")
    if level not in["Junior", "Middle", "Senior"]:
        raise CandidateLevelError(
            f"The candidate's level must be equal to one of: Junior, Middle, Senior but was {level}!"
        )
    return True


def assignment_description_is_valid(description: str) -> bool:
    pattern = r"^[a-zA-Z\[\],.!?\(\)@#%:;\"']+$"

    if not bool(re.match(pattern, description)):
        raise ValidCharactersError(
            "The text contains invalid characters! Use only latin a-z A-Z, and next symbols: [],.!?()@#%:;\"'"
        )

    if len(description) > 2500:
        raise LengthError("Max length of description must be 2500 symbols")

    return True


def git_url_is_valid(url: str):
    base_url = "https://github.com"
    if not url.startswith(base_url):
        raise GitHubDomainError(f"url must start with {base_url}")



if __name__ == "__main__":
    print(candidate_level_is_valid("Junior"))
    print(candidate_level_is_valid("Middle"))
    print(candidate_level_is_valid("Senior"))
    print(candidate_level_is_valid([1, 2, 3]))
