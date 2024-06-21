from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import UserModel

from .repository import user_repository
from .schemas import UserCreate, UserGet, UserGetWithPassword
from .utils import get_password_hash


class UserService:
    async def create_user(
        self,
        async_session: AsyncSession,
        data: UserCreate,
    ) -> UserGet:
        user_data = data.model_dump()
        user = await user_repository.create(
            async_session=async_session,
            data={
                "username": user_data["username"],
                "email": user_data["email"],
                "hashed_password": get_password_hash(user_data["password"]),
            },
        )
        return UserGet(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
        )

    async def get_users(
        self,
        async_session: AsyncSession,
        order: str = "id",
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserGet]:
        users = await user_repository.get_all(
            async_session=async_session,
            order=order,
            offset=offset,
            limit=limit,
        )
        return [
            UserGet(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
            )
            for user in users
        ]

    async def get_user_by_id(
        self,
        async_session: AsyncSession,
        user_id: int,
    ) -> UserGet | None:
        user: UserModel | None = await user_repository.get(
            async_session=async_session,
            id=user_id,
        )

        if user:
            return UserGet(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
            )

    async def get_user_by_username(
        self,
        async_session: AsyncSession,
        username: str,
    ) -> UserGet | None:
        user: UserModel | None = await user_repository.get(
            async_session=async_session,
            username=username,
        )
        if user:
            return UserGet(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
            )

    async def get_user_by_username_with_password(
        self,
        async_session: AsyncSession,
        username: str,
    ) -> UserGetWithPassword | None:
        user: UserModel | None = await user_repository.get(
            async_session=async_session,
            username=username,
        )
        if user:
            return UserGetWithPassword(
                id=user.id,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
                is_active=user.is_active,
            )


    async def delete_user(
        self,
        async_session: AsyncSession,
        user_id: int,
    ) -> None:
        await user_repository.delete(
            async_session=async_session,
            id=user_id,
        )


user_service = UserService()
