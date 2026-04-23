import time
from sqlalchemy.exc import OperationalError
import os

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

def create_engine_with_retry():
    url = os.getenv("DATABASE_URL")
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

