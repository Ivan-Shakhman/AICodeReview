import exeptions
from fastapi.responses import JSONResponse
from fastapi import Request


async def description_error_handler(request: Request, exc: exeptions.DescriptionError):
    return JSONResponse(
        status_code=400,
        content={"message": f"Oops! {exc.message}"},
    )


async def candidate_level_error_handler(request: Request, exc: exeptions.CandidateLevelError):
    return JSONResponse(
        status_code=400,
        content={"message": f"Oops! {exc.message}"},
    )


async def git_hub_domain_error_handler(request: Request, exc: exeptions.GitHubDomainError):
    return JSONResponse(
        status_code=400,
        content={"message": f"Oops! {exc.message}"},
    )

