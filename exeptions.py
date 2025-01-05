"""Custom exceptions for readability in logging"""


class BaseCustomException(Exception):
    def __init__(self, message: str):
        self.message = message


class CandidateLevelError(BaseCustomException):
    pass


class DescriptionError(BaseCustomException):
    pass


class GitHubDomainError(BaseCustomException):
    pass
