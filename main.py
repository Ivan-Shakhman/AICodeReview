import os
from engine import SessionLocal
from fastapi import FastAPI
from sqlalchemy.orm import Session
from repo_extractor import download_all_branches
from exeptions import (
    CandidateLevelError,
    DescriptionError,
    GitHubDomainError
)
from handlers import (
    candidate_level_error_handler,
    description_error_handler,
    git_hub_domain_error_handler,
)
from models import ReviewBodyBase
from validators import (
    assignment_description_is_valid,
    candidate_level_is_valid,
    git_url_is_valid,
)
from openai_worker import analyze_repo
import logging


logger = logging.getLogger("uvicorn")

app = FastAPI()

"""add handlers to app"""
app.add_exception_handler(CandidateLevelError, candidate_level_error_handler)
app.add_exception_handler(DescriptionError, description_error_handler)
app.add_exception_handler(GitHubDomainError, git_hub_domain_error_handler)


def get_db() -> Session:
    """don't need right now but for future scaling must have"""
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def title_screen():
    return {
        "message": "Welcome to code review endpoint! To start work"
        " you need to use POST-method in json format with next data:"
        "assignment_description: short description of your github project(please note! "
        "Dont use special symbols like &^ and other); "
        "git_repo_url: url for your repository; "
        "open_api_key: APIkey for using openAI; "
        "candidate_level: write one of your level: Junior, Middle or Senior"
    }


@app.post("/")
async def make_code_review(review_input: ReviewBodyBase):
    if all(
            (
            git_url_is_valid(review_input.git_repo_url),
            assignment_description_is_valid(review_input.assignment_description),
            candidate_level_is_valid(review_input.candidate_level)
            )
    ):
        logger.info("Validate successfully")
        download_all_branches(review_input.git_repo_url)
        result = analyze_repo(
            description=review_input.assignment_description,
            level=review_input.candidate_level,
            api_key=review_input.open_api_key
        )
        logger.info("Response is success 200 OK")
        return {"Review": result}

    logger.error("Client error 400. Invalid input data!")
