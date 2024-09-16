from typing import Sequence
from uuid import UUID

from sqlalchemy import select, or_, and_
from sqlalchemy.orm import joinedload

from app.models import Employee, OrganizationResponsible
from app.models.bid import Bid, BidHistory
from app.repositories.base import BaseRepository
from app.schemas.bid_schema import BidStatus


class BidRepository(BaseRepository):
    model = Bid

    async def add_bid(self, **data) -> model:
        return await self._add_one(**data)

    async def get_bid_by_id(self, bid_id: UUID) -> model | None:
        return await self._get_one(id=bid_id)

    async def edit_bid(self, bid_id: UUID, **data) -> model:
        return await self._edit_one(bid_id, **data)

    async def get_bids_by_username(
            self,
            username: str,
            limit: int,
            offset: int,
            order_by: str = "name"
    ) -> Sequence[model]:
        stmt = (
            select(self.model)
            .join(Employee, self.model.author_id == Employee.id)
            .where(Employee.username == username)
            .order_by(order_by)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_bids_by_tender_id_and_username(
            self,
            tender_id: UUID,
            organization_id: UUID,
            limit: int,
            offset: int,
            order_by: str = "name"
    ) -> Sequence[model]:
        subquery = select(OrganizationResponsible.user_id).where(
            OrganizationResponsible.organization_id == organization_id
        )
        stmt = (
            select(Bid)
            .where(Bid.tender_id == tender_id)
            .where(
                or_(
                    Bid.author_id.in_(subquery),
                    Bid.author_id == organization_id,
                    Bid.status == BidStatus.published
                )
            )
            .order_by(order_by)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_bid_for_submit_decision(self, bid_id: UUID) -> model:
        stmt = (select(self.model)
                .options(joinedload(self.model.tender))
                .where(Bid.id == bid_id)
                )
        return await self.session.scalar(stmt)


class BidHistoryRepository(BaseRepository):
    model = BidHistory

    async def add_bid_history(self, **data) -> model:
        return await self._add_one(**data)

    async def get_bid_history(self, bid_id: UUID, version: int) -> model:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.bid))
            .where(and_(self.model.bid_id == bid_id, self.model.version == version))
        )
        return await self.session.scalar(stmt)
