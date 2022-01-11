"""
Post path opertaions

    Raises:
        HTTPException: [description]
        this: [description]
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

# pylint: disable=invalid-name

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """
    Create a new post
    """

    return crud.create_post(db=db, post=post)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
      Retrieve all posts.
      Allows for pagination
    """
    posts = crud.get_posts(db=db, skip=skip, limit=limit)
    return posts


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific post based on post_id
    """
    post = crud.get_post(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with post_id={post_id} does not exist in db!")
    return post


@ router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    """
    Update a post
    """

    updated_post = crud.update_post(db=db, post=post, post_id=post_id)

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id={post_id} does not exist!')

    return updated_post


@ router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Delete a post
    """
    deleted_post = crud.delete_post(db=db, post_id=post_id)

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id={post_id} does not exist!')

    return Response(status_code=status.HTTP_204_NO_CONTENT)
