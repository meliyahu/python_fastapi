"""
Api routes

    Raises:
        HTTPException: [description]
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
# pylint: disable=invalid-name

import logging
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, get_db

logging.basicConfig(filename='fastapi.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    """
    FastApi
    Returns:
        JSON: Api greetings
    """
    return {"message": "FastApi is alive!"}


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """
    Create a new post
    """

    return crud.create_post(db=db, post=post)


@app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
      Retrieve all posts.
      Allows for pagination
    """
    posts = crud.get_posts(db=db, skip=skip, limit=limit)
    return posts


@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific post based on post_id
    """
    post = crud.get_post(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with post_id={post_id} does not exist in db!")
    return post


@ app.put("/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    """
    Update a post
    """

    updated_post = crud.update_post(db=db, post=post, post_id=post_id)

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id={post_id} does not exist!')

    return updated_post


@ app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Delete a post
    """
    deleted_post = crud.delete_post(db=db, post_id=post_id)

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id={post_id} does not exist!')

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create user path operation

    Args:
        user (schemas.User): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).
    """
    created_user = crud.create_user(db=db, user=user)

    if created_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User with email={user.email} exist already!')

    return created_user


@app.get("/users", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
     Get list of users path operation
    """
    return crud.get_users(db=db, skip=skip, limit=limit)


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get s

    Args:
        user_id (int): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id:{user_id} does not exist!')
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete user path operation

    Args:
        user_id (int): [description]
    """
    user = crud.delete_user(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id: {user_id} does not exist!')

    return Response(status_code=status.HTTP_204_NO_CONTENT)
