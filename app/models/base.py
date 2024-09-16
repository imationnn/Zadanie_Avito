import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import text, UUID


created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=text("TIMEZONE('utc', now())"))
]


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    @declared_attr
    def __tablename__(self) -> str:
        """
        Changes the table name from "CamelCase" to "camel_cases"
        :return:
        """
        table_name = str()
        for char in self.__name__:
            if char.isupper():
                if table_name:
                    table_name += "_"
                char = char.lower()
            table_name += char
        return table_name
