"""
    Pydantic models for data from/to api
"""
# pylint: disable=too-few-public-methods
# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from pydantic import BaseModel


class PostBase(BaseModel):
    """
    Post base class

    Args:
        BaseModel ([type]): BaseModel class
    """
    title: str
    content: str
    published: bool = True


class PostCreate(BaseModel):
    """
    A create Post class

    Args:
        BaseModel ([type]): [description]
    """


class Post(PostBase):
    """
    A post pydantic class
    """
    id: int

    class Config:
        """
        ORM config class
        """
        orm_mode = True
