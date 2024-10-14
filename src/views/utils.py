from fastapi import Depends
from sqlalchemy import insert
from fastapi_cache.decorator import cache

import httpx

from database import AsyncSession, get_async_session
from views.models import catalog
from config import KP_TOKEN, KP_URL, MAL_URL


@cache(expire=30)
async def additional_search(title: str, series: bool = False, session: AsyncSession = Depends(get_async_session)):
    response_title = None

    data = await request_to_API(KP_URL, title)
    for record in data["docs"]:
        if record["isSeries"] == series and record["alternativeName"] == title:
            response_title = record["alternativeName"]
            response_year = record["year"]
            break
    
    if not response_title:
        data = await request_to_API(MAL_URL, title, api='mal')
        for record in data["data"]:
            if record["title"] == title:
                response_title = record["title"]
                response_year = record["year"]
                break           

    if not response_title:
        return None
                
    stmt = insert(catalog).values(title=response_title, release_year=response_year, is_series=series)
    result = await session.execute(stmt)
    cat_id, = result.inserted_primary_key
    await session.commit()

    return cat_id


@cache(expire=30)
async def request_to_API(link, title, api='kp'):
    headers = {
        'accept': 'application/json',
    }
    params = {
        'page': 1,
        'limit': 5,
    }
    if api == 'kp':
        headers['X-API-KEY'] = KP_TOKEN
        params['query'] = title
    else:
        params['q'] = title

    async with httpx.AsyncClient() as client:
        response = await client.get(
            link, params=params, headers=headers, timeout=10
        )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.status_code, response.text)


#@cache(expire=30)
async def create_response(status, data, details) -> dict:
    response = {
        "status": status,
        "data": data,
        "details": details
    }
    return response


class Paginator:
    def __init__(self, limit: int = 5, offset: int = 0) -> None:
        self.limit = limit
        self.offset = offset