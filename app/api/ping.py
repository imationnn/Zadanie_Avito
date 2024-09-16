from fastapi import APIRouter


ping_router = APIRouter()


@ping_router.get(
    "/ping",
    summary="Проверка доступности сервера",
    description="Этот эндпоинт используется для проверки готовности сервера обрабатывать запросы.\n\n"
                "Чекер программа будет ждать первый успешный ответ и затем начнет выполнение тестовых сценариев.",
    responses={
        200: {
            "description": "Сервер готов обрабатывать запросы, если отвечает '200 OK'.",
            "content": {
              "text/plain": {
                 "example": "ok"
              }
            }
        },
        500: {
          "description": "Сервер не готов обрабатывать запросы, если ответ статусом 500 или любой другой, кроме 200."
        }
    }
)
async def get_ping() -> str:
    return "ok"
