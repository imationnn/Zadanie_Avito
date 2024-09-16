from uuid import UUID

from app.models.organization import Organization
from app.repositories.base import BaseRepository


class OrganizationRepository(BaseRepository):
    model = Organization

    async def get_organization_by_id(self, organization_id: UUID) -> model | None:
        return await self._get_one(id=organization_id)
