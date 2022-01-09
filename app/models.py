"""
    ORM models
"""
from sqlalchemy import Boolean, Column, Integer, String
# from sqlalchemy.orm import relationship
from app.database import Base


class Post(Base):
    """
    An orm class representing the posts database table

    Args:
        Base ([type]): [description]
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, default=True)
