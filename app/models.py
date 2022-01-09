"""
    ORM models
"""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
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
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=text('now()'))


class User(Base):
    """
    User orm class

    Args:
        Base ([type]): [description]
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
