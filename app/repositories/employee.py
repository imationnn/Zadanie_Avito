from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload, aliased

from app.models import OrganizationResponsible
from app.models.employee import Employee
from app.repositories.base import BaseRepository


class EmployeeRepository(BaseRepository):
    model = Employee

    async def get_employee(self, **filters) -> model | None:
        stmt = (select(self.model)
                .options(joinedload(self.model.organizations))
                .filter_by(**filters)
                )
        return await self.session.scalar(stmt)

    async def get_employees_organization(
            self,
            user_id1: UUID,
            user_id2: UUID
    ) -> OrganizationResponsible.organization_id | None:
        o1 = aliased(OrganizationResponsible)
        o2 = aliased(OrganizationResponsible)
        stmt = (
            select(o1.organization_id)
            .join(o2,
                  o1.organization_id == o2.organization_id)
            .filter(
                o1.user_id == user_id1,
                o2.user_id == user_id2
            )
        )
        return await self.session.scalar(stmt)
