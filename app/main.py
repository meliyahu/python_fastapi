"""
Api routes

    Raises:
        HTTPException: [description]
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """

import logging

from fastapi import FastAPI
from .routers import post, user, auth
from . import models
from .database import engine

logging.basicConfig(filename='fastapi.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def fast_api_root():
    """
    FastApi\n
    Returns:
        JSON: Api greetings
    """
    return {"message": "FastApi is alive!"}
