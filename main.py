from fastapi import FastAPI
from sqlalchemy.orm import Session

from engine import SessionLocal
from exeptions import CandidateLevelError, DescriptionError, GitHubDomainError
from handlers import candidate_level_error_handler, description_error_handler, git_hub_domain_error_handler
from models import ReviewBodyBase
from validators import assignment_description_is_valid, candidate_level_is_valid, git_url_is_valid

app = FastAPI()

app.add_exception_handler(CandidateLevelError, candidate_level_error_handler)
app.add_exception_handler(DescriptionError, description_error_handler)
app.add_exception_handler(GitHubDomainError, git_hub_domain_error_handler)


def get_db() -> Session:
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def title_screen():
    return {"message": "Welcome to code review endpoint!"}


@app.post("/")
async def make_code_review(review_input: ReviewBodyBase):
    assignment_description_is_valid(review_input.assignment_description)
    candidate_level_is_valid(review_input.candidate_level)
    git_url_is_valid(review_input.git_repo_url)

    return {"message": "Item created successfully", "item": review_input}
