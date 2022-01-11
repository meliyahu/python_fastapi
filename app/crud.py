"""
    Utility methods to implememnt CRUD
"""
from sqlalchemy.orm import Session

from . import models, schemas, utils

# pylint: disable=invalid-name


def create_post(db: Session, post: schemas.PostCreate):
    """
     Util method to create a post
    Args:
        db (Session): A db session object
        post (schemas.PostCreate): Post to create

    Returns:
        Post: the newly created post
    """
    # update_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    """
    Util method to get list of posts

    Args:
        db (Session): [description]
        skip (int, optional): Offset. Defaults to 0.
        limit (int, optional): Limit. Defaults to 10.

    Returns:
        models.Post: Zero or One or more posts
    """
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int):
    """
    Util method to get a single post based on id

    Args:
        db (Session): [description]
        post_id (int): [description]

    Returns:
        model.Post: [description]
    """
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def update_post(db: Session, post: schemas.Post, post_id: int):
    """
    Unit method to update a post

    Args:
        db (Session): [description]
        post (schemas.Post): [description]
        post_id (int): [description]
    """
    # 1. Retrieve post from db
    updated_post = db.query(models.Post).filter(
        models.Post.id == post_id).first()
    if updated_post is None:
        return None

    # 2. Update post fields
    updated_post.title = post.title
    updated_post.content = post.content
    updated_post.published = post.published

    # 3. Save post in db
    # db.flush()
    db.commit()
    db.refresh(updated_post)
    return updated_post


def delete_post(db: Session, post_id: int):
    """
    Delete post

    Args:
        db (Session): [description]
        post_id (int): [description]

    Returns:
        Post: delete post or None if post is not in db
    """
    deleted_post = db.query(models.Post).filter(
        models.Post.id == post_id).first()

    if deleted_post is None:
        return None

    db.delete(deleted_post)
    db.commit()
    return deleted_post


def create_user(db: Session, user: schemas.User):
    """
    Create user

    Args:
        db (Session): [description]
        user (schemas.User): [description]
    """
    # Check if user exists
    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if db_user is not None:
        return None

    # hash the password
    user.password = utils.hash_pswd(user.password)
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit=10):
    """
    Retrieve list of users

    Args:
        db (Session): [description]
        skip (int, optional): [description]. Defaults to 0.
        limit (int, optional): [description]. Defaults to 10.

    Returns:
        [type]: [description]
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    """
    Get single users

    Args:
        db (Session): [description]
        user_id (int): [description]
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


def delete_user(db: Session, user_id):
    """
    Delete user

    Args:
        db (Session): [description]
        user_id ([type]): [description]
    """
    user = db.query(models.User).filter(
        models.User.id == user_id).first()

    if user is None:
        return None

    db.delete(user)
    db.commit()
    return user


def user_login(db: Session, user: schemas.UserLogin):
    """
    For user login

    Args:
        db (Session): [description]
        user (schemas.UserLogin): [description]
    """
    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    return db_user
