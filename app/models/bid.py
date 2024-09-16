from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text

from app.models.base import Base, created_at
from app.models.tender import Tender
from app.schemas.bid_schema import BidStatus


class Bid(Base):
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(default=BidStatus.created)
    tender_id: Mapped[UUID] = mapped_column(ForeignKey(Tender.id))
    author_type: Mapped[str]
    author_id: Mapped[UUID]
    version: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[created_at]

    historical_bids = relationship("BidHistory", back_populates="bid")
    tender: Mapped["Tender"] = relationship("Tender")


class BidHistory(Base):
    __tablename__ = 'bid_histories'

    bid_id: Mapped[UUID] = mapped_column(ForeignKey(Bid.id))
    version: Mapped[int]
    name: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[created_at]

    bid = relationship("Bid", back_populates="historical_bids")
