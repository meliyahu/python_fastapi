"""
    Utils module

    Returns:
        [type]: [description]
    """
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def hash_pswd(password: str):
    """
    Hashing function

    Args:
        password (str): [description]

    Returns:
        [type]: [description]
    """
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str):
    """
    Verify plain password to hashed_password

    Args:
        plain_password (str): [description]
        hashed_password (bool): [description]

    Returns:
        [type]: [description]
    """
    return pwd_context.verify(plain_password, hashed_password)
