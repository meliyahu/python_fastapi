"""
    Utility methods to implememnt CRUD
"""
from sqlalchemy.orm import Session
from .models_shemas import models, schemas

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
    # db_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


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
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        return None

    # 2. Update post fields
    db_post.title = post.title
    db_post.content = post.content
    db_post.published = post.published

    # 3. Save post in db
    # db.flush()
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    """
    Delete post

    Args:
        db (Session): [description]
        post_id (int): [description]

    Returns:
        Post: delete post or None if post is not in db
    """
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if db_post is None:
        return None

    db.delete(db_post)
    return db_post
