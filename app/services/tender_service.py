from uuid import UUID

from fastapi import Depends

from app.models import Tender
from app.repositories.tender import TenderRepository, TenderHistoryRepository
from app.services.employee_service import EmployeeService
from app.schemas.tender_schema import NewTender, TenderOut, TenderStatus, EditTender
from app.exceptions.exceptions import TenderNotFound, NotEnoughRights, BadParametersPassed, TenderOrVersionNotFound
from app.utils import model_to_dict


class TenderService:
    def __init__(
            self,
            tender_repository: TenderRepository = Depends(),
            tender_history_repository: TenderHistoryRepository = Depends(),
            employee_service: EmployeeService = Depends()
    ):
        self.tender_repository = tender_repository
        self.tender_history_repository = tender_history_repository
        self.employee_service = employee_service

    async def add_tender(self, tender: NewTender) -> TenderOut:
        employee = await self.employee_service.check_and_return_employee_belongs_to_organization_by_username(
            tender.creator_username,
            tender.organization_id
        )
        new_tender = await self.tender_repository.add_tender(
            **tender.model_dump(exclude={'creator_username'}),
            employee_id=employee.id
        )
        await self.tender_history_repository.add_tender_history(
            **model_to_dict(new_tender, "id", "status", "created_at"),
            tender_id=new_tender.id,
        )
        await self.tender_repository.session.commit()
        return TenderOut.model_validate(new_tender)

    async def get_published_tenders(
            self,
            limit: int,
            offset: int,
            service_type: list[str] | None = None
    ) -> list[TenderOut]:
        result = await self.tender_repository.get_published_tenders(limit, offset, service_type)
        return [TenderOut.model_validate(tender) for tender in result]

    async def get_tenders_for_current_user(
            self,
            limit: int,
            offset: int,
            username: str
    ) -> list[TenderOut]:
        if username is None:
            return await self.get_published_tenders(limit, offset)
        result = await self.tender_repository.get_tender_by_username(username, limit, offset)
        return [TenderOut.model_validate(tender) for tender in result]

    async def get_tender_by_id(self, tender_id: UUID) -> Tender:
        tender = await self.tender_repository.get_tender_by_id(tender_id)
        if tender is None:
            raise TenderNotFound
        return tender

    async def get_tender_status_by_tender_id(self, tender_id: UUID, username: str) -> TenderStatus:
        tender = await self.get_tender_by_id(tender_id)
        if username is not None:
            employee = await self.employee_service.get_employee(username=username)
            if self.employee_service.check_employee_belongs_to_organization(tender.organization_id, employee):
                return tender.status
        if tender.status == TenderStatus.published:
            return tender.status
        raise NotEnoughRights

    async def _get_tender_with_check_user(self, tender_id: UUID, username: str) -> Tender:
        tender = await self.get_tender_by_id(tender_id)
        await self.employee_service.check_and_return_employee_belongs_to_organization_by_username(
            username,
            tender.organization_id
        )
        return tender

    async def change_tender_status(
            self,
            tender_id: UUID,
            status: str,
            username: str
    ) -> TenderOut:
        tender = await self._get_tender_with_check_user(tender_id, username)
        tender.status = status
        await self.tender_repository.session.commit()
        return TenderOut.model_validate(tender)

    async def edit_tender(
            self,
            edit_fields: EditTender,
            tender_id: UUID,
            username: str
    ) -> TenderOut:
        edit_fields = edit_fields.model_dump(exclude_none=True)
        if not edit_fields:
            raise BadParametersPassed
        tender = await self._get_tender_with_check_user(tender_id, username)
        tender.version += 1
        await self.tender_repository.edit_tender(tender_id, **edit_fields, version=tender.version)
        await self.tender_history_repository.add_tender_history(
            **model_to_dict(tender, "id", "status", "created_at"),
            tender_id=tender.id,
        )
        await self.tender_repository.session.commit()
        return TenderOut.model_validate(tender)

    async def rollback_tender_version(self, tender_id: UUID, version: int, username: str) -> TenderOut:
        tender_history = await self.tender_history_repository.get_tender_history(tender_id, version)
        if not tender_history:
            raise TenderOrVersionNotFound
        await self.employee_service.check_and_return_employee_belongs_to_organization_by_username(
            username,
            tender_history.organization_id
        )
        tender_history.tender.version += 1
        tender_history.tender.description = tender_history.description
        tender_history.tender.service_type = tender_history.service_type
        tender_history.tender.name = tender_history.name
        await self.tender_history_repository.add_tender_history(
            **model_to_dict(tender_history, "id", "status", "created_at", "version"),
            version=tender_history.tender.version
        )
        await self.tender_repository.session.commit()
        return TenderOut.model_validate(tender_history.tender)

    async def check_published_tender_by_id(self, tender_id: UUID) -> Tender:
        tender = await self.get_tender_by_id(tender_id)
        if tender.status != TenderStatus.published:
            raise BadParametersPassed
        return tender
