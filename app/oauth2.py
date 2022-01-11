"""
    autho functions
    """
from datetime import datetime, timedelta

# from hashlib import algorithms_guaranteed
# from jose import JWTError, jwt
from jose import jwt

# SECRET_KEY
SECRET_KEY = "90c01196a4ceac9b6f24e72bd6a382d4ba7c5a5917de582fd9712cec3bc52cfa"
# Algorithm
ALGORITHM = "HS256"
# Expriry time of token
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """

    Creat token
    Args:
        data (dict): [description]
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
