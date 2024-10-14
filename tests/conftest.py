import asyncio
import pytest

from typing import AsyncGenerator

from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from fastapi.testclient import TestClient
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src import metadata
from src.main import app
from src.config import *
from src.database import get_async_session


#!!!USE VAR BELOW FOR TEST BASE!!!
# DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

#!!!TEMP CONNECTION TO MAIN BASE, COMMENT THIS IF USE TEST BASE!!!
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session    


#!!!USE FIXTURE BELOW FOR TEST BASE!!!
# @pytest.fixture(autouse=True, scope='session')
# async def prepare_database():
#     async with engine_test.begin() as conn:
#         await conn.run_sync(metadata.create_all)
#     yield
#     async with engine_test.begin() as conn:
#         await conn.run_sync(metadata.drop_all)   


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def a_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as a_client:
        yield a_client


@pytest.fixture(autouse=True, scope='session')
def fastapi_cache():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")