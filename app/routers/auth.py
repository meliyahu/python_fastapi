"""
    Login router

    Raises:
        HTTPException: [description]
    """
from fastapi import APIRouter, Depends, HTTPException, status #, Response
from sqlalchemy.orm import Session
from app import crud, schemas, utils, oauth2
from app.database import get_db

router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)

# pylint: disable=invalid-name


@router.post('/')
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Login to get authorisation token

    Args:
        user (schemas.UserLogin): [description]
        db (Session, optional): [description]. Defaults to Depends(get_db).
    """
    db_user = crud.user_login(db=db, user=user)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid credentials!')

    # Get hash pass from db
    # hash incoming plain password
    # If not valid return error
    # If valid generate JWT token and send back to user.
    if not utils.verify(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid credentials!')

     # Create a token and return to user
    access_token = oauth2.create_access_token(data={"user_id": db_user.id})
    return {"token": access_token}
