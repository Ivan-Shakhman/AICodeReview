from pydantic import BaseModel


class ReviewBodyBase(BaseModel):
    assignment_description: str
    git_repo_url: str
    open_api_key: str
    candidate_level: str
