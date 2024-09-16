from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import Field

from app.schemas.base_schema import BaseSchema


class ServiceType(str, Enum):
    construction = "Construction"
    delivery = "Delivery"
    manufacture = "Manufacture"


class TenderStatus(str, Enum):
    created = "Created"
    published = "Published"
    closed = "Closed"


class TenderOut(BaseSchema):
    id: UUID = Field(
        description="Уникальный идентификатор тендера, присвоенный сервером.",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )
    name: str = Field(
        description="Полное название тендера",
        examples=["Доставка товары Казань - Москва"]
    )
    description: str = Field(
        description="Описание тендера",
        examples=["Нужно доставить оборудование для олимпиады по робототехнике"]
    )
    service_type: ServiceType = Field(description="Вид услуги, к которой относится тендер")
    status: TenderStatus = Field(description="Статус тендера")
    version: int = Field(default=1, description="Версия тендера")
    created_at: datetime = Field(
        description="Серверная дата и время в момент, когда пользователь отправил тендер на создание",
        examples=["2006-01-02T15:04:05Z07:00"]
    )


class NewTender(BaseSchema):
    name: str = Field(max_length=100, description="Полное название тендера")
    description: str = Field(max_length=500, description="Описание тендера")
    service_type: ServiceType = Field(description="Вид услуги, к которой относится тендер")
    organization_id: UUID = Field(
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="Уникальный идентификатор организации, присвоенный сервером."
    )
    creator_username: str = Field(
        examples=["test_user"],
        description="Уникальный slug пользователя."
    )


class EditTender(BaseSchema):
    name: str | None = Field(None, max_length=100, description="Полное название тендера")
    description: str | None = Field(None, max_length=500, description="Описание тендера")
    service_type: ServiceType | None = Field(None, description="Вид услуги, к которой относится тендер")
