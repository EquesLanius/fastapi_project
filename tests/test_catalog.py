from httpx import AsyncClient
from conftest import fastapi_cache

async def test_corr_add_to_catalog(a_client: AsyncClient):
    response = await a_client.post("/catalog", json={
        "title": "Test",
        "release_year": 2002,
        "is_series": False
    })

    assert response.status_code == 200


async def test_incorr_type_add_to_catalog(a_client: AsyncClient):
    response = await a_client.post("/catalog", json={
        "title": 312312,
        "release_year": 2002,
        "is_series": False
    })

    assert response.status_code == 422


async def test_duplicate_add_to_catalog(a_client: AsyncClient):
    response = await a_client.post("/catalog", json={
        "title": "Test",
        "release_year": 2002,
        "is_series": False
    })

    assert response.status_code == 404


async def test_search_exist_in_catalog(a_client: AsyncClient, fastapi_cache):
    response = await a_client.get("/catalog", params={
        "search_title": "Test",
    })

    assert response.status_code == 200


async def test_search_notexist_in_catalog(a_client: AsyncClient, fastapi_cache):
    response = await a_client.get("/catalog", params={
        "search_title": "NOT_EXIST",
    })

    assert response.status_code == 404