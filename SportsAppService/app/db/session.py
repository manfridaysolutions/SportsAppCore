import time
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings

def create_engine_with_retry():
    url = settings.database_url
    retries = 10
    delay = 3

    for attempt in range(retries):
        try:
            engine = create_async_engine(url, echo=True)
            return engine
        except OperationalError:
            print(f"Database not ready, retrying {attempt+1}/{retries}")
            time.sleep(delay)

    raise Exception("Could not connect to database after multiple attempts.")

engine = create_engine_with_retry()

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

