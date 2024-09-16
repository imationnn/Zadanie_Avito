import asyncio
import logging

from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tenacity import retry, stop_after_attempt, wait_fixed

from app.database import db_connector
from app.models import Employee, Tender
from app.models.base import Base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_TRIES = 7
WAIT_SECONDS = 1.5


@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
)
async def init_db(session: AsyncSession):
    try:
        await session.execute(select(1))
    except Exception as err:
        logger.error(err)
        raise err


async def check_and_create_migration(session: AsyncSession):
    try:
        await session.execute(select(Employee))
        await session.execute(select(Tender))
    except ProgrammingError:
        await session.rollback()
        logger.info("Creating tables")
        async with db_connector.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    logger.info("Generating needed data")


async def main():
    async with db_connector.session_factory() as session:
        logger.info("Initializing database")
        await init_db(session)
        await check_and_create_migration(session)


if __name__ == '__main__':
    asyncio.run(main())
