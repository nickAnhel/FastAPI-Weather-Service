from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from .service import user_service
from .utils import encode_jwt
from .schemas import (
    UserCreate,
    UserGet,
    UserGetWithPassword,
    Token,
)
from .dependencies import (
    authenticate_user,
    get_current_user,
    get_current_active_user,
)

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# Auth endpoints
@auth_router.post("/register")
async def register(
    data: UserCreate,
    async_session: AsyncSession = Depends(get_async_session),
) -> UserGet:
    try:
        return await user_service.create_user(async_session=async_session, data=data)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        ) from exc


@auth_router.post("/login")
def login(
    user: UserGetWithPassword = Depends(authenticate_user),
) -> Token:
    access_token = encode_jwt(
        payload={
            "sub": user.id,
            "username": user.username,
            "email": user.email,
        },
    )

    return Token(
        access_token=access_token,
        token_type="Bearer",
    )


# User endpoints
@user_router.get("")
async def get_users(
    order: str = "id",
    offset: int = 0,
    limit: int = 100,
    async_session: AsyncSession = Depends(get_async_session),
) -> list[UserGet]:
    return await user_service.get_users(
        async_session=async_session,
        order=order,
        offset=offset,
        limit=limit,
    )


@user_router.get("/me")
def get_current_user_info(
    user: UserGet = Depends(get_current_active_user),
) -> UserGet:
    return user


@user_router.get("/user")
async def get_user_by_id(
    user_id: int,
    async_session: AsyncSession = Depends(get_async_session),
) -> UserGet:
    if not (
        user := await user_service.get_user_by_id(
            async_session=async_session,
            user_id=user_id,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@user_router.get("/user/{username}")
async def get_user_by_username(
    username: str,
    async_session: AsyncSession = Depends(get_async_session),
) -> UserGet:
    if not (
        user := await user_service.get_user_by_username(
            async_session=async_session,
            username=username,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@user_router.delete("/user")
async def delete_user(
    # user_id: int,
    current_user: UserGet = Depends(get_current_user),
    async_session: AsyncSession = Depends(get_async_session),
) -> None:
    await user_service.delete_user(
        async_session=async_session,
        user_id=current_user.id,
    )
