from pydantic import BaseModel
from typing import Optional
'''
A schema class to force clients to create valid posts
'''
class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None    