from exeptions import (
    CandidateLevelError,
    DescriptionError,
    GitHubDomainError,
)
import re
import logging
logger = logging.getLogger("uvicorn")


def candidate_level_is_valid(level: str) -> bool:
    logger.info("Validate level of candidate")
    if not level:
        logger.error("Level must be not empty!")
        raise CandidateLevelError(message="Level must be not empty!")

    if type(level) is not str:
        logger.error(f"Type of level is {type(level)} but must be str!")
        raise CandidateLevelError(
            message=f"Type of level is {type(level)} but must be str!"
        )

    if level not in ["Junior", "Middle", "Senior"]:
        logger.error(f"The candidate's level must be equal to one of: Junior, Middle, Senior but was {level}!")
        raise CandidateLevelError(
            message=f"The candidate's level must be equal to one of: Junior, Middle, Senior but was {level}!"
        )

    return True


def assignment_description_is_valid(description: str) -> bool:
    pattern = r"^[a-zA-Z\[\],.!?\(\)@%:;\"'\s]+$"
    logger.info("Validate assignment description")
    if not description:
        logger.error("Description must be not empty!")
        raise DescriptionError(message="Description must be not empty!")

    if not bool(re.match(pattern, description)):
        logger.error("The text contains invalid characters! Use only latin a-z A-Z, and next symbols: [],.!?()@#%:;\"'")
        raise DescriptionError(
            message="The text contains invalid characters! Use only latin a-z A-Z, and next symbols: [],.!?()@#%:;\"'"
        )

    if len(description) > 2500:
        logger.error("Description is too long")
        raise DescriptionError(message="Max length of description must be 2500 symbols")

    return True


def git_url_is_valid(url: str) -> bool:
    base_url = "https://github.com/"
    exc = ".git"
    logger.info("Validate github url")
    if not url:
        logger.error("url must be not empty!")
        raise GitHubDomainError(message="url must be not empty!")

    if not url.startswith(base_url):
        logger.error(f"url must start with {base_url}!")
        raise GitHubDomainError(message=f"url must start with {base_url}!")

    if not url.endswith(exc):
        logger.error(f"url must end with {exc}!")
        raise GitHubDomainError(message=f"url must end with {exc}!")
    return True
