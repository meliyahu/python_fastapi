"""
    Pydantic models for data from/to api
"""

# pylint: disable=too-few-public-methods
# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# from typing import Any
from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    """
    Post base class

    Args:
        BaseModel ([type]): BaseModel class
    """
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    """
    A create Post class

    Args:
        BaseModel ([type]): [description]
    """


class PostUpdate(PostBase):
    """
    Update post

    Args:
        PostBase ([type]): [description]
    """


class Post(PostBase):
    """
    A post pydantic class
    """
    id: int
    created_at: datetime

    class Config:
        """
        ORM config class
        """
        orm_mode = True


class UserBase(BaseModel):
    """
    A user schema class

    Args:
        BaseModel ([type]): [description]
    """
    email: EmailStr


class UserCreate(UserBase):
    """
    Create user schema

    Args:
        UserBase ([type]): [description]
    """
    password: str

class UserLogin(UserBase):
    """
    Login user schema

    Args:
        UserBase ([type]): [description]
    """
    password: str


class User(UserBase):
    """
    User schema

    Args:
        UserBase ([type]): [description]
    """
    id: int
    created_at: datetime

    class Config:
        """
          orm fisher
        """
        orm_mode = True
