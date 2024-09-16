from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.models.base import Base, created_at
from app.models.organization import Organization
from app.models.employee import Employee
from app.schemas.tender_schema import TenderStatus


class Tender(Base):
    name: Mapped[str]
    description: Mapped[str]
    service_type: Mapped[str]
    status: Mapped[str] = mapped_column(default=TenderStatus.created)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey(Organization.id, ondelete="CASCADE"))
    employee_id: Mapped[UUID] = mapped_column(ForeignKey(Employee.id))
    version: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[created_at]

    historical_versions = relationship("TenderHistory", back_populates="tender")


class TenderHistory(Base):
    __tablename__ = 'tender_histories'

    tender_id: Mapped[UUID] = mapped_column(ForeignKey(Tender.id))
    version: Mapped[int]
    name: Mapped[str]
    description: Mapped[str]
    service_type: Mapped[str]
    organization_id: Mapped[UUID]
    employee_id: Mapped[UUID]
    created_at: Mapped[created_at]

    tender = relationship("Tender", back_populates="historical_versions")
