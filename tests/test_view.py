from httpx import AsyncClient


async def test_add_to_view(a_client: AsyncClient):
    response = await a_client.post("/view/add", json={
        "title": "Test",
        "view_date": "2024-10-10",
        "season": 0,
        "episode": 0
    })

    assert response.status_code == 200


async def test_add_to_view_already_exist(a_client: AsyncClient):
    response = await a_client.post("/view/add", json={
        "title": "Test",
        "view_date": "2024-10-10",
        "season": 0,
        "episode": 0
    })

    assert response.status_code == 404


async def test_search_exist_in_view(a_client: AsyncClient):
    response = await a_client.get("/view/search", params={
        "search_title": "Test",
    })

    assert response.status_code == 200


async def test_search_notexist_in_view(a_client: AsyncClient):
    response = await a_client.get("/view/search", params={
        "search_title": "NOT_EXIST",
    })

    assert response.status_code == 404