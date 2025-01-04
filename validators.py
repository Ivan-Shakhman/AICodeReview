from exeptions import CandidateLevelError


def validate_candidate_level(level: str) -> bool:
    if type(level) is not str:
        raise TypeError(f"Type of level is {type(level)} but must be str!")
    if level not in["Junior", "Middle", "Senior"]:
        raise CandidateLevelError(
            f"The candidate's level must be equal to one of: Junior, Middle, Senior but was {level}!"
        )
    return True


if __name__ == "__main__":
    print(validate_candidate_level("Junior"))
    print(validate_candidate_level("Middle"))
    print(validate_candidate_level("Senior"))
    print(validate_candidate_level([1, 2, 3]))
