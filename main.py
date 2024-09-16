from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import main_router
from app.pre_start import main


@asynccontextmanager
async def lifespan(_):
    await main()
    yield


app = FastAPI(
    lifespan=lifespan,
    version="1.0",
    title="Tender Management API",
    description="API для управления тендерами и предложениями.\n\n"
                "Основные функции API включают управление тендерами (создание, изменение, получение списка) и "
                "управление предложениями (создание, изменение, получение списка)."
)


app.include_router(main_router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
