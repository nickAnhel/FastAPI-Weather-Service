from typing import Any
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserModel


class UserRepository:
    async def create(
        self,
        async_session: AsyncSession,
        data: dict[str, Any],
    ) -> UserModel:
        user = UserModel(**data)
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)
        return user

    async def get(
        self,
        async_session: AsyncSession,
        **filters,
    ) -> UserModel | None:
        query = (
            select(UserModel)
            .filter_by(**filters)
        )
        result = await async_session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def get_all(
        self,
        async_session: AsyncSession,
        order: str = "id",
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserModel]:
        query = (
            select(UserModel)
            .order_by(order)
            .offset(offset)
            .limit(limit)
        )
        result = await async_session.execute(query)
        users = list(result.scalars().all())
        return users

    async def update(
        self,
        async_session: AsyncSession,
        data: dict[str, Any],
        **filters,
    ) -> UserModel | None:
        stmt = (
            update(UserModel)
            .filter_by(**filters)
            .values(**data)
            .returning(UserModel)
        )
        result = await async_session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def delete(
        self,
        async_session: AsyncSession,
        **filters,
    ) -> None:
        stmt = (
            delete(UserModel)
            .filter_by(**filters)
        )
        await async_session.execute(stmt)
        await async_session.commit()


user_repository = UserRepository()
