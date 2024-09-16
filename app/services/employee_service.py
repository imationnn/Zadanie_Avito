from uuid import UUID

from fastapi import Depends

from app.models import OrganizationResponsible
from app.repositories.employee import EmployeeRepository
from app.exceptions.exceptions import NotEnoughRights, UserNotExistOrInvalid


class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository = Depends()):
        self.employee_repository = employee_repository

    async def check_and_return_employee_belongs_to_organization(
            self,
            organization_id: UUID,
            **filters
    ) -> EmployeeRepository.model:
        employee = await self.get_employee(**filters)
        if not self.check_employee_belongs_to_organization(organization_id, employee):
            raise NotEnoughRights
        return employee

    async def check_and_return_employee_belongs_to_organization_by_username(
            self,
            username: str,
            organization_id: UUID
    ) -> EmployeeRepository.model:
        return await self.check_and_return_employee_belongs_to_organization(
            organization_id,
            username=username
        )

    async def check_and_return_employee_belongs_to_organization_by_id(
            self,
            user_id: UUID,
            organization_id: UUID
    ) -> EmployeeRepository.model:
        return await self.check_and_return_employee_belongs_to_organization(
            organization_id,
            id=user_id
        )

    @staticmethod
    def check_employee_belongs_to_organization(
            organization_id: UUID,
            employee: EmployeeRepository.model
    ) -> bool:
        return any(org_resp.organization_id == organization_id for org_resp in employee.organizations)

    async def get_employee(self, **filters) -> EmployeeRepository.model:
        employee = await self.employee_repository.get_employee(**filters)
        if not employee:
            raise UserNotExistOrInvalid
        return employee

    async def check_and_return_organization_by_user_ids(
            self,
            user_id1: UUID,
            user_id2: UUID
    ) -> OrganizationResponsible.organization_id | None:
        return await self.employee_repository.get_employees_organization(user_id1, user_id2)
