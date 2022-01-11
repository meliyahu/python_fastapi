"""
User path opertaions

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

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# pylint: disable=invalid-name


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
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


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
     Get list of users path operation
    """
    return crud.get_users(db=db, skip=skip, limit=limit)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user

    Args:
        user_id (int): The user id to search for

    Raises:
        HTTPException: May raise this exception if user does not exist in the database

    Returns:
        (User): User json object
    """
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id:{user_id} does not exist!')
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
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
