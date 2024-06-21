from typing import Any
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError

from ..database import get_async_session
from .utils import decode_jwt, validate_password
from .service import user_service
from .schemas import UserGet, UserGetWithPassword


# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


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
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> dict[str, Any]:
    # token = credentials.credentials
    try:
        return decode_jwt(token)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        ) from exc


async def get_current_user(
    payload: dict[str, Any] = Depends(_get_token_payload),
    async_session: AsyncSession = Depends(get_async_session),
) -> UserGet:
    if not (
        user := await user_service.get_user_by_username(
            async_session=async_session,
            username=payload.get("username"),  # type: ignore
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authorization token",
        )

    return user


def get_current_active_user(
    current_user: UserGet = Depends(get_current_user),
) -> UserGet:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return current_user
