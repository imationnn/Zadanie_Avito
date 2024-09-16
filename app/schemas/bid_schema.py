from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import Field

from app.schemas.base_schema import BaseSchema


class BidStatus(str, Enum):
    created = "Created"
    published = "Published"
    canceled = "Canceled"


class AuthorType(str, Enum):
    organization = "Organization"
    user = "User"


class BidStatusDecision(str, Enum):
    approved = "Approved"
    rejected = "Rejected"


class BidOut(BaseSchema):
    id: UUID = Field(
        description="Уникальный идентификатор предложения, присвоенный сервером",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )
    name: str = Field(
        description="Полное название предложения",
        examples=["Доставка товаров Алексей"]
    )
    description: str = Field(
        description="Описание предложения",
        examples=["Доставка оборудования для олимпиады по робототехнике"]
    )
    status: BidStatus | BidStatusDecision = Field(description="Статус предложения")
    author_type: AuthorType = Field(description="Тип автора")
    author_id: UUID = Field(description="Уникальный идентификатор автора предложения, присвоенный сервером")
    version: int = Field(default=1, description="Номер версии")
    created_at: datetime = Field(
        description="Серверная дата и время в момент, когда пользователь отправил предложение на создание",
        examples=["2006-01-02T15:04:05Z07:00"]
    )


class NewBid(BaseSchema):
    name: str = Field(max_length=100, description="Полное название предложения")
    description: str = Field(max_length=500, description="Описание предложения")
    tender_id: UUID = Field(
        description="Уникальный идентификатор тендера, присвоенный сервером.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    author_type: AuthorType = Field(description="Тип автора")
    author_id: UUID = Field(
        description="Уникальный идентификатор автора предложения, присвоенный сервером",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )


class EditBid(BaseSchema):
    name: str | None = Field(max_length=100, description="Полное название предложения")
    description: str | None = Field(max_length=500, description="Описание предложения")


class BidOutDecision(BidOut):
    status: BidStatusDecision = Field(description="Статус предложения")
