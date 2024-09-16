from uuid import UUID

from fastapi import Depends

from app.models import Bid
from app.repositories.bid import BidRepository, BidHistoryRepository
from app.repositories.organization import OrganizationRepository
from app.schemas.bid_schema import NewBid, BidOut, AuthorType, BidStatus, EditBid, BidOutDecision, BidStatusDecision
from app.schemas.tender_schema import TenderStatus
from app.services.employee_service import EmployeeService
from app.services.tender_service import TenderService
from app.exceptions.exceptions import (
    NotEnoughRights,
    BadParametersPassed,
    OrganizationNotFound,
    TenderOrBidNotFound,
    BidNotFound,
    BidOrVersionNotFound
)


class BidService:
    def __init__(
            self,
            bid_repository: BidRepository = Depends(),
            bid_history_repository: BidHistoryRepository = Depends(),
            employee_service: EmployeeService = Depends(),
            tender_service: TenderService = Depends(),
            organization_repository: OrganizationRepository = Depends()
    ):
        self.bid_repository = bid_repository
        self.bid_history_repository = bid_history_repository
        self.employee_service = employee_service
        self.tender_service = tender_service
        self.organization_repository = organization_repository

    async def _check_author_for_create_bid(
            self,
            author_id: UUID,
            organization_id: UUID,
            author_type: str
    ) -> None:
        if author_type == AuthorType.user:
            employee = await self.employee_service.get_employee(id=author_id)
            if self.employee_service.check_employee_belongs_to_organization(organization_id, employee):
                raise NotEnoughRights
        else:
            if organization_id == author_id:
                raise NotEnoughRights
            if not await self.organization_repository.get_organization_by_id(author_id):
                raise OrganizationNotFound

    async def add_bid(self, bid: NewBid) -> BidOut:
        tender = await self.tender_service.check_published_tender_by_id(bid.tender_id)
        await self._check_author_for_create_bid(bid.author_id, tender.organization_id, bid.author_type)
        new_bid = await self.bid_repository.add_bid(**bid.model_dump())
        await self.bid_history_repository.add_bid_history(
            name=new_bid.name,
            description=new_bid.description,
            version=new_bid.version,
            bid_id=new_bid.id
        )
        await self.bid_repository.session.commit()
        return BidOut.model_validate(new_bid)

    async def get_bids_for_current_user(
            self,
            limit: int,
            offset: int,
            username: str
    ) -> list[BidOut]:
        result = await self.bid_repository.get_bids_by_username(username, limit, offset)
        return [BidOut.model_validate(bid) for bid in result]

    async def get_bids_by_tender_id(
            self,
            tender_id: UUID,
            username: str,
            limit: int,
            offset: int,
    ) -> list[BidOut]:
        employee = await self.employee_service.get_employee(username=username)
        result = await self.bid_repository.get_bids_by_tender_id_and_username(
            tender_id,
            employee.organizations[0].organization_id if employee.organizations else None,
            limit,
            offset
        )
        if not result:
            raise TenderOrBidNotFound
        return [BidOut.model_validate(bid) for bid in result]

    async def get_bid_by_id(self, bid_id: UUID) -> BidRepository.model:
        bid = await self.bid_repository.get_bid_by_id(bid_id)
        if bid is None:
            raise BidNotFound
        return bid

    async def get_bid_status_by_bid_id(self, bid_id: UUID, username: str) -> BidStatus:
        bid = await self.get_bid_by_id(bid_id)
        if bid.status != BidStatus.published:
            await self.check_user_rights_for_actions_with_bid(bid, username)
        return bid.status

    async def change_bid_status(self, bid_id: UUID, status: str, username: str) -> BidOut:
        bid = await self.get_bid_by_bid_id_and_check_user_rights(bid_id, username)
        bid.status = status
        await self.bid_repository.session.commit()
        return BidOut.model_validate(bid)

    async def edit_bid(
            self,
            edit_fields: EditBid,
            bid_id: UUID,
            username: str
    ) -> BidOut:
        edit_fields = edit_fields.model_dump(exclude_none=True)
        if not edit_fields:
            raise BadParametersPassed
        bid = await self.get_bid_by_bid_id_and_check_user_rights(bid_id, username)
        bid.version += 1
        await self.bid_repository.edit_bid(bid_id, **edit_fields, version=bid.version)
        await self.bid_history_repository.add_bid_history(
            name=bid.name,
            description=bid.description,
            version=bid.version,
            bid_id=bid.id
        )
        await self.bid_repository.session.commit()
        return BidOut.model_validate(bid)

    async def get_bid_submit_decision(
            self,
            bid_id: UUID,
            decision: str,
            username: str
    ) -> BidOutDecision:
        bid = await self.bid_repository.get_bid_for_submit_decision(bid_id)
        if not bid:
            raise BidNotFound

        if bid.status != BidStatus.published or bid.tender.status != TenderStatus.published:
            raise NotEnoughRights

        await self.employee_service.check_and_return_employee_belongs_to_organization_by_username(
            username,
            bid.tender.organization_id
        )
        bid.status = decision
        if bid.status == BidStatusDecision.approved:
            bid.tender.status = TenderStatus.closed
        await self.bid_repository.session.commit()
        return BidOutDecision.model_validate(bid)

    async def select_check_user_by_autor_type(
            self,
            bid: Bid,
            username: str
    ) -> bool:
        employee = await self.employee_service.get_employee(username=username)

        if bid.author_type == AuthorType.organization:
            if self.employee_service.check_employee_belongs_to_organization(bid.author_id, employee):
                return True
        elif bid.author_type == AuthorType.user:
            if await self.employee_service.check_and_return_organization_by_user_ids(employee.id, bid.author_id):
                return True

        return False

    async def check_user_rights_for_actions_with_bid(self, bid: Bid, username: str) -> None:
        if not await self.select_check_user_by_autor_type(bid, username):
            raise NotEnoughRights

    async def get_bid_by_bid_id_and_check_user_rights(self, bid_id: UUID, username: str) -> Bid:
        bid = await self.get_bid_by_id(bid_id)
        await self.check_user_rights_for_actions_with_bid(bid, username)
        return bid

    async def rollback_bid_version(self, bid_id: UUID, version: int, username: str) -> BidOut:
        bid_history = await self.bid_history_repository.get_bid_history(bid_id, version)
        if not bid_history:
            raise BidOrVersionNotFound

        await self.check_user_rights_for_actions_with_bid(bid_history.bid, username)
        bid_history.bid.version += 1
        bid_history.bid.description = bid_history.description
        bid_history.bid.name = bid_history.name

        await self.bid_history_repository.add_bid_history(
            name=bid_history.bid.name,
            description=bid_history.bid.description,
            version=bid_history.bid.version,
            bid_id=bid_history.bid.id
        )
        await self.bid_repository.session.commit()
        return BidOut.model_validate(bid_history.bid)
