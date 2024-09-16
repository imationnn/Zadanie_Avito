from typing import Sequence
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from app.models.tender import Tender, TenderHistory
from app.models.employee import Employee
from app.repositories.base import BaseRepository
from app.schemas.tender_schema import TenderStatus


class TenderRepository(BaseRepository):
    model = Tender

    async def add_tender(self, **data) -> model:
        return await self._add_one(**data)

    async def get_tender_by_id(self, tender_id: UUID) -> model | None:
        return await self._get_one(id=tender_id)

    async def edit_tender(self, tender_id: UUID, **data) -> model:
        return await self._edit_one(tender_id, **data)

    async def get_published_tenders(
            self,
            limit: int,
            offset: int,
            service_type: list[str] | None = None,
            order_by: str = "name"
    ) -> Sequence[model]:
        filters = [self.model.status == TenderStatus.published]
        if service_type is not None:
            filters.append(self.model.service_type.in_(service_type))
        return await self._get_multi(
            *filters,
            order=order_by,
            limit=limit,
            offset=offset
        )

    async def get_tender_by_username(
            self,
            username: str,
            limit: int,
            offset: int,
            order_by: str = "name"
    ) -> Sequence[model]:
        stmt = (
            select(self.model)
            .join(Employee, self.model.employee_id == Employee.id)
            .where(Employee.username == username)
            .order_by(order_by)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.scalars(stmt)
        return result.all()


class TenderHistoryRepository(BaseRepository):
    model = TenderHistory

    async def add_tender_history(self, **data) -> model:
        return await self._add_one(**data)

    async def get_tender_history(self, tender_id: UUID, version: int) -> model:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.tender))
            .where(and_(self.model.tender_id == tender_id, self.model.version == version))
        )
        return await self.session.scalar(stmt)
