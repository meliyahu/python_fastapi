"""
A schema class to force clients to create valid posts
    """
from typing import Optional

# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from pydantic import BaseModel


class Post(BaseModel):
    """[summary]

    Args:
        BaseModel ([type]): [description]
    """
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
