import enum
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey

from app.models.base import Base, created_at, updated_at
from app.models.employee import Employee


class OrganizationType(enum.Enum):
    IE = "IE",
    LLC = "LLC",
    JSC = "JSC"


class Organization(Base):

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    type: Mapped[OrganizationType | None]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    responsibilities: Mapped[list["OrganizationResponsible"]] = relationship(
        "OrganizationResponsible",
        back_populates="organization"
    )


class OrganizationResponsible(Base):

    organization_id: Mapped[UUID | None] = mapped_column(ForeignKey(Organization.id, ondelete="CASCADE"))
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey(Employee.id, ondelete="CASCADE"))

    organization: Mapped["Organization"] = relationship("Organization", back_populates="responsibilities")
    user: Mapped["Employee"] = relationship("Employee", back_populates="organizations")
