from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


"""can be used in future if app start scale and add authentication"""
SQLALCHEMY_DATABASE_URL = "sqlite:///./review.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autoflush=False, autocomit=False, bind=engine)

Base = declarative_base()
