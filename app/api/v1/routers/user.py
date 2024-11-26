from logging import getLogger
from typing import Dict, Literal

from core.authentication.auth_middleware import (
    authenticate_user,
    get_current_active_user,
)
from core.authentication.auth_token import create_access_token
from core.storage import storage
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import User, UserIn, UserOut

router = APIRouter()


@router.post(path="/register", response_model=UserOut)
def register_user(input: UserIn) -> UserOut:
    """Registers a new user"""
    logger = getLogger(__name__ + ".register_user")

    try:
        id = storage.user_create_record(user_data=input, verified=True)

        return storage.user_verify_record({"_id": id})

    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex),
            )
        raise ex


@router.post(
    path="/login",
    response_model=Dict[
        Literal["access_token", "token_type", "username", "email", "user_id"],
        str,
    ],
)
def login_user(input: OAuth2PasswordRequestForm = Depends()) -> UserOut:
    """Logs in a user"""
    logger = getLogger(__name__ + ".login_user")

    try:
        user = authenticate_user(email=input.username, password=input.password)

        logger.info("User Authenticated")
        if not user.verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account not verified",
            )

        logger.info(f"User ({user.id}) Verified")
        token_data = {
            "sub": user.email,
            "id": user.id,
            "role": user.role,
            "type": "bearer",
        }
        access_token = create_access_token(token_data)
        logger.info(f"User ({user.id}) Token Generated")

        return JSONResponse(
            {
                "access_token": access_token,
                "token_type": "bearer",
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            }
        )

    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex),
            )
        raise ex


@router.get(path="/users/me", response_model=UserOut)
def get_user_details(
    current_user: User = Depends(get_current_active_user),
) -> UserOut:
    """Gets the details of the logged in user"""
    logger = getLogger(__name__ + ".login_user")
    try:
        return current_user

    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex),
            )
        raise ex
