from typing import Any
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import (
    # OAuth2PasswordBearer,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError

from ..database import get_async_session
from .utils import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD, decode_jwt, validate_password
from .service import user_service
from .schemas import UserGet, UserGetWithPassword


http_bearer = HTTPBearer()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def authenticate_user(
    username: str = Form(...),
    password: str = Form(...),
    async_session: AsyncSession = Depends(get_async_session),
) -> UserGetWithPassword:
    user = await user_service.get_user_by_username_with_password(
        async_session=async_session,
        username=username,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
        )

    if not validate_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


def _get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    # token: str = Depends(oauth2_scheme),
) -> dict[str, Any]:
    token = credentials.credentials
    try:
        return decode_jwt(token)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc


def _get_current_user_by_token_type(token_type: str):
    async def get_current_user_by_token_type_wrapper(
        payload: dict[str, Any] = Depends(_get_token_payload),
        async_session: AsyncSession = Depends(get_async_session),
    ) -> UserGet:
        given_token_type = payload.get(TOKEN_TYPE_FIELD)
        if not given_token_type == token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type {given_token_type!r}, excepted {token_type!r}",
            )

        if not (
            user := await user_service.get_user_by_id(
                async_session=async_session,
                user_id=payload.get("sub"),  # type: ignore
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization token",
            )

        return user

    return get_current_user_by_token_type_wrapper


get_current_user = _get_current_user_by_token_type(ACCESS_TOKEN_TYPE)
get_current_user_for_refresh = _get_current_user_by_token_type(REFRESH_TOKEN_TYPE)


def get_current_active_user(
    current_user: UserGet = Depends(get_current_user),
) -> UserGet:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return current_user
