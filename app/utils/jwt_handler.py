from datetime import timedelta, datetime, timezone

from jose import JWTError, jwt

from config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': email, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(email: str, user_id: int, expires_delta: timedelta):
    """
    Create a refresh token for a user.

    Args:
        email (str): User's email.
        user_id (int): User's ID.
        expires_delta (timedelta): Duration for which the refresh token is valid.

    Returns:
        str: Encoded JWT refresh token.
    """
    encode = {'sub': email, 'id': user_id, 'type': 'refresh'}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)



def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
