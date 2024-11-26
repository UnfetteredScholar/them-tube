from datetime import UTC, datetime, timedelta
from typing import Any, Dict, Union

from core.config import settings
from fastapi import HTTPException, status
from jose import JWTError, jwt
from schemas.token import TokenData

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(
    data: Dict[str, Any], expires_delta: Union[timedelta, None] = None
) -> str:
    """
    Creates a jwt access token using the data provided

    Args:
        data: data to be encoded into the token
        expires_delta: period of time which the token will be valid

    Returns:
        encoded jwt string
    """

    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            days=settings.ACCESS_TOKEN_EXPIRE_DAYS
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str) -> TokenData:
    """
    Verifies an access token

    Args:
        token: the jwt token string

    Returns:
        TokenData object containing the data in the token
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        id = payload.get("id")
        token_type: str = payload.get("type")

        if email is None or id is None:
            raise credentials_exception

        return TokenData(email=email, id=id, type=token_type)
    except JWTError:
        raise credentials_exception
