from typing import Sequence
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update

from app.database import db_connector
from app.models.base import Base


class BaseRepository:
    model: type[Base]

    def __init__(self, session: AsyncSession = Depends(db_connector.get_session)):
        self.session = session

    async def _get_one(self, **filter_by) -> Base | None:
        stmt = select(self.model).filter_by(**filter_by)
        return await self.session.scalar(stmt)

    async def _get_multi(self, *filters,  order: str = "id", limit: int = 100, offset: int = 0) -> Sequence:
        stmt = select(self.model).filter(*filters).order_by(order).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return result.all()

    async def _add_one(self, **data):
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def _edit_one(self, _id: UUID, **data):
        stmt = update(self.model).values(**data).filter_by(id=_id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()
