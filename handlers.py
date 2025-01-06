import exeptions
from fastapi.responses import JSONResponse
from fastapi import Request


async def description_error_handler(request: Request, exc: exeptions.DescriptionError):
    """handle errors when description from user is not valid"""
    return JSONResponse(
        status_code=400,
        content={"message": f"Oops! {exc.message}"},
    )


async def candidate_level_error_handler(
    request: Request, exc: exeptions.CandidateLevelError
):
    """handle errors when candidate level from user incorrect"""
    return JSONResponse(
        status_code=400,
        content={"message": f"Oops! {exc.message}"},
    )


async def git_hub_domain_error_handler(
    request: Request, exc: exeptions.GitHubDomainError
):
    """handle errors if link to github don't start with https://github.com"""
    return JSONResponse(
        status_code=400,
        content={"message": f"Oops! {exc.message}"},
    )
