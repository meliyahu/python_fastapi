"""
Module containing database connection for the api
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use sqlite for testing - local db file
# SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# Use postgres for production
# TODO: get postgresql uri from config file
SQLALCHEMY_DATABASE_URL = "postgresql://fastapi:fastapi@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency

# pylint: disable=invalid-name


def get_db():
    """
    Dependency method to get db session
    for each request and closed after each
    request
    Yields:
        Session: db session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
