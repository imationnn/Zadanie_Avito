from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from app.models.base import Base, created_at, updated_at


if TYPE_CHECKING:
    from app.models.organization import Organization


class Employee(Base):

    username: Mapped[str] = mapped_column(String(50), unique=True)
    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    organizations: Mapped[list["Organization"]] = relationship(
        "OrganizationResponsible",
        back_populates="user"
    )
