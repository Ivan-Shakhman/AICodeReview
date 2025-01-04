from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()


@app.post("/")
async def make_code_review(

        db: Session = Depends(get_db)

):
    pass
