from uuid import UUID

from fastapi import APIRouter, Depends, Query, Path

from app.schemas.tender_schema import NewTender, TenderOut, EditTender, TenderStatus, ServiceType
from app.services.tender_service import TenderService
from app.api.responses import (
    error400,
    error401,
    error403,
    error404_tender_not_found,
    error404_tender_or_version_not_found,
    error422,
    error500
)


tender_router = APIRouter(prefix="/tenders")


@tender_router.get(
    "",
    summary="Получение списка тендеров",
    description="Список тендеров с возможностью фильтрации по типу услуг.\n\n"
                "Если фильтры не заданы, возвращаются все тендеры.",
    response_description="Список тендеров, отсортированных по алфавиту по названию.",
    responses={
        422: error422,
        500: error500
    }
)
async def get_tenders(
        limit: int | None = Query(
            5,
            description="Максимальное число возвращаемых объектов.\nИспользуется для запросов с пагинацией."
        ),
        offset: int | None = Query(
            0,
            description="Какое количество объектов должно быть пропущено с начала.\n"
                        "Используется для запросов с пагинацией."
        ),
        service_type: list[ServiceType] = Query(
            None,
            description="Возвращенные тендеры должны соответствовать указанным видам услуг.\n\n"
                        "Если список пустой, фильтры не применяются."
        ),
        tender_service: TenderService = Depends()
) -> list[TenderOut]:
    return await tender_service.get_published_tenders(limit, offset, service_type)


@tender_router.post(
    "/new",
    summary="Создание нового тендера",
    description="Создание нового тендера с заданными параметрами.",
    response_description="Тендер успешно создан. Сервер присваивает уникальный идентификатор и время создания.",
    responses={
        401: error401,
        403: error403,
        422: error422,
        500: error500
    }
)
async def add_tender(
        tender: NewTender,
        tender_service: TenderService = Depends()
) -> TenderOut:
    return await tender_service.add_tender(tender)


@tender_router.get(
    "/my",
    summary="Получить тендеры пользователя",
    description="Получение списка тендеров текущего пользователя.\n"
                "Для удобства использования включена поддержка пагинации.",
    response_description="Список тендеров пользователя, отсортированный по алфавиту.",
    responses={
        422: error422,
        500: error500
    }
)
async def get_tenders_by_username(
        limit: int | None = Query(
            5,
            description="Максимальное число возвращаемых объектов.\nИспользуется для запросов с пагинацией."
        ),
        offset: int | None = Query(
            0,
            description="Какое количество объектов должно быть пропущено с начала.\n"
                        "Используется для запросов с пагинацией."
        ),
        username: str | None = Query(None),
        tender_service: TenderService = Depends()
) -> list[TenderOut]:
    return await tender_service.get_tenders_for_current_user(limit, offset, username)


@tender_router.get(
    "/{tenderId}/status",
    summary="Получение текущего статуса тендера",
    description="Получить статус тендера по его уникальному идентификатору.",
    response_description="Текущий статус тендера.",
    responses={
        401: error401,
        403: error403,
        404: error404_tender_not_found,
        422: error422,
        500: error500
    }
)
async def get_tender_status(
        tender_id: UUID = Path(alias="tenderId"),
        username: str | None = Query(None),
        tender_service: TenderService = Depends()
) -> TenderStatus:
    return await tender_service.get_tender_status_by_tender_id(tender_id, username)


@tender_router.put(
    "/{tenderId}/status",
    summary="Изменения статуса тендера",
    description="Изменить статус тендера по его идентификатору",
    response_description="Статус тендера успешно изменен.",
    responses={
        401: error401,
        403: error403,
        404: error404_tender_not_found,
        422: error422,
        500: error500
    }
)
async def change_tender_status(
        tender_id: UUID = Path(alias="tenderId"),
        status: TenderStatus = Query(),
        username: str = Query(),
        tender_service: TenderService = Depends()
) -> TenderOut:
    return await tender_service.change_tender_status(tender_id, status, username)


@tender_router.patch(
    "/{tenderId}/edit",
    summary="Редактирование тендера",
    description="Изменение параметров существующего тендера.",
    response_description="Тендер успешно изменен и возвращает обновленную информацию.",
    responses={
        400: error400,
        401: error401,
        403: error403,
        404: error404_tender_not_found,
        422: error422,
        500: error500
    }
)
async def edit_tender(
        edit_fields: EditTender,
        tender_id: UUID = Path(alias="tenderId",),
        username: str = Query(),
        tender_service: TenderService = Depends()
) -> TenderOut:
    return await tender_service.edit_tender(edit_fields, tender_id, username)


@tender_router.put(
    "/{tenderId}/rollback/{version}",
    summary="Откат версии тендера",
    description="Откатить параметры тендера к указанной версии. "
                "Это считается новой правкой, поэтому версия инкрементируется.",
    response_description="Тендер успешно откачен и версия инкрементирована.",
    responses={
        401: error401,
        403: error403,
        404: error404_tender_or_version_not_found,
        422: error422,
        500: error500
    }
)
async def rollback_tender_version(
        tender_id: UUID = Path(alias="tenderId"),
        version: int = Path(description="Номер версии, к которой нужно откатить тендер"),
        username: str = Query(),
        tender_service: TenderService = Depends()
) -> TenderOut:
    return await tender_service.rollback_tender_version(tender_id, version, username)
