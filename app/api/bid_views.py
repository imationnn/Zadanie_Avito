from uuid import UUID

from fastapi import APIRouter, Depends, Query, Path

from app.schemas.bid_schema import NewBid, BidOut, BidStatus, EditBid, BidOutDecision, BidStatusDecision
from app.services.bid_service import BidService
from app.api.responses import (
    error400,
    error401,
    error403,
    error404_bid_not_found,
    error404_bid_or_version_not_found,
    error404_tender_not_found,
    error404_tender_or_bid_not_found,
    error422,
    error500
)


bid_router = APIRouter(prefix="/bids")


@bid_router.post(
    "/new",
    summary="Создание нового предложения",
    description="Создание предложения для существующего тендера.",
    response_description="Предложение успешно создано. Сервер присваивает уникальный идентификатор и время создания",
    responses={
        400: error400,
        401: error401,
        403: error403,
        404: error404_tender_not_found,
        422: error422,
        500: error500
    }
)
async def add_bid(
        bid: NewBid,
        bid_service: BidService = Depends()
) -> BidOut:
    return await bid_service.add_bid(bid)


@bid_router.get(
    "/my",
    summary="Получение списка ваших предложений",
    description="Получение списка предложений текущего пользователя.\n\n"
                "Для удобства использования включена поддержка пагинации.",
    response_description="Список предложений пользователя, отсортированный по алфавиту.",
    responses={
        422: error422,
        500: error500
    }
)
async def get_bids_by_username(
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
        bid_service: BidService = Depends()
) -> list[BidOut]:
    return await bid_service.get_bids_for_current_user(limit, offset, username)


@bid_router.get(
    "/{tenderId}/list",
    summary="Получение списка предложений для тендера",
    description="Получение предложений, связанных с указанным тендером.",
    response_description="Список предложений, отсортированный по алфавиту.",
    responses={
        401: error401,
        404: error404_tender_or_bid_not_found,
        422: error422,
        500: error500
    }
)
async def get_bids_by_tender_id(
        tender_id: UUID = Path(alias="tenderId"),
        username: str = Query(),
        limit: int | None = Query(
            5,
            description="Максимальное число возвращаемых объектов.\nИспользуется для запросов с пагинацией."
        ),
        offset: int | None = Query(
            0,
            description="Какое количество объектов должно быть пропущено с начала.\n"
                        "Используется для запросов с пагинацией."
        ),
        bid_service: BidService = Depends()
) -> list[BidOut]:
    return await bid_service.get_bids_by_tender_id(tender_id, username, limit, offset)


@bid_router.get(
    "/{bidId}/status",
    summary="Получение текущего статуса предложения",
    description="Получить статус предложения по его уникальному идентификатору.",
    response_description="Текущий статус предложения",
    responses={
        401: error401,
        403: error403,
        404: error404_bid_not_found,
        422: error422,
        500: error500
    }
)
async def get_bid_status(
        bid_id: UUID = Path(alias="bidId"),
        username: str = Query(),
        bid_service: BidService = Depends()
) -> BidStatus | BidStatusDecision:
    return await bid_service.get_bid_status_by_bid_id(bid_id, username)


@bid_router.put(
    "/{bidId}/status",
    summary="Изменение статуса предложения",
    description="Изменить статус предложения по его уникальному идентификатору.",
    response_description="Статус предложения успешно изменен",
    responses={
        401: error401,
        403: error403,
        404: error404_bid_not_found,
        422: error422,
        500: error500
    }
)
async def change_bid_status(
        bid_id: UUID = Path(alias="bidId"),
        status: BidStatus = Query(),
        username: str = Query(),
        bid_service: BidService = Depends()
) -> BidOut:
    return await bid_service.change_bid_status(bid_id, status, username)


@bid_router.patch(
    "/{bidId}/edit",
    summary="Редактирование параметров предложения.",
    description="Редактирование существующего предложения.",
    response_description="Предложение успешно изменено и возвращает обновленную информацию",
    responses={
        400: error400,
        401: error401,
        403: error403,
        404: error404_bid_not_found,
        422: error422,
        500: error500
    }
)
async def edit_bid(
        edit_fields: EditBid,
        bid_id: UUID = Path(alias="bidId"),
        username: str = Query(),
        bid_service: BidService = Depends()
) -> BidOut:
    return await bid_service.edit_bid(edit_fields, bid_id, username)


@bid_router.put(
    "/{bidId}/submit_decision",
    summary="Отправка решения по предложению",
    description="Отправить решение (одобрить или отклонить) по предложению.",
    response_description="Решение по предложению успешно отправлено",
    responses={
        401: error401,
        403: error403,
        404: error404_bid_not_found,
        422: error422,
        500: error500
    }
)
async def submit_decision(
        bid_id: UUID = Path(alias="bidId"),
        decision: BidStatusDecision = Query(),
        username: str = Query(),
        bid_service: BidService = Depends()
) -> BidOutDecision:
    return await bid_service.get_bid_submit_decision(bid_id, decision, username)


@bid_router.put(
    "/{bidId}/rollback/{version}",
    summary="Откат версии предложения",
    description="Откатить параметры предложения к указанной версии. "
                "Это считается новой правкой, поэтому версия инкрементируется.",
    response_description="Предложение успешно откатано и версия инкрементирована",
    responses={
        401: error401,
        403: error403,
        404: error404_bid_or_version_not_found,
        422: error422,
        500: error500
    }
)
async def rollback_bid_version(
        tender_id: UUID = Path(alias="bidId"),
        version: int = Path(),
        username: str = Query(),
        bid_service: BidService = Depends()
) -> BidOut:
    return await bid_service.rollback_bid_version(tender_id, version, username)
