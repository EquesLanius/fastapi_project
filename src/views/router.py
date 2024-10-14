from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql import text
from sqlalchemy import select, insert

from fastapi_cache.decorator import cache

from database import AsyncSession, get_async_session

from views.querys import *
from views.utils import additional_search, create_response, Paginator
from views.models import catalog, view
from views.schemas import CatalogRecord, ResponseCatalog, NewView, ResponseView, ResponseAddView

from auth.models import User
from auth.base_config import current_user, current_superuser


router_for_su = APIRouter(
    prefix="/catalog",
    tags=["Catalog management"],
    dependencies=[Depends(current_superuser)]
)


router = APIRouter(
    prefix="/view",
    tags=["User views"],
)


@router_for_su.get("", response_model=ResponseCatalog)
@cache(expire=30)
async def get_specific_record(search_title: str, session: AsyncSession = Depends(get_async_session)) -> dict:
    query = select(catalog).where(catalog.c.title == search_title)
    result = await session.execute(query)
    data = result.mappings().all()
    if data == []:
        raise HTTPException(status_code=404, detail=await create_response("error", data, "not found"))

    return await create_response("success", data, "found")


@router_for_su.get("/all", response_model=ResponseCatalog)
@cache(expire=30)
async def get_all_catalog(
    pgn: Paginator = Depends(Paginator),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    
    query = select(catalog).limit(pgn.limit).offset(pgn.offset)
    result = await session.execute(query)
    data = result.mappings().all()
    if data == []:
        raise HTTPException(status_code=404, detail=await create_response("error", data, "not found"))
    
    return await create_response("success", data, "catalog records")


@router_for_su.post("", response_model=ResponseCatalog)
async def add_to_catalog(
    record: CatalogRecord,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    
    data = record.model_dump()
    query = await query_exist_cat(data['title'], data['release_year'], data['is_series'])
    result = await session.execute(text(query))
    check = result.mappings().all()   
    await session.commit()
    if check == []:
        raise HTTPException(status_code=404, detail=await create_response("error", data, "already exist"))

    return await create_response("success", [data], "added")


@router.post("/add", response_model=ResponseAddView)
async def add_to_views(
    new_view: NewView,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> dict:
    
    data = new_view.model_dump()
    if data["season"] != 0:
        series = True
    else:
        series = False    
    
    query = select(catalog).where((catalog.c.title == data["title"]) & (catalog.c.is_series == series))
    search = await session.execute(query)
    search_res = search.mappings().all()

    if search_res == []:
        cat_id = await additional_search(title=data["title"], series=series, session=session)
    else:
        cat_id = search_res[0]["id"]    

    if not cat_id:
        raise HTTPException(status_code=404, detail=await create_response("error", data["title"], "non-existent/incorrect title"))

    query = await query_exist_view(user.id, cat_id, data["view_date"], data["season"], data["episode"])
    result = await session.execute(text(query))
    check = result.mappings().all()
    await session.commit()
    if check == []:
        raise HTTPException(status_code=404, detail=await create_response("error", [], "already exist"))
    
    return await create_response("success", data, "added")


@router.get("/all", response_model=ResponseView)
async def get_all_user_views(
    pgn: Paginator = Depends(Paginator),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> dict:
    
    query = await query_user_views(user.id, pgn.limit, pgn.offset)
    result = await session.execute(text(query))
    data = result.mappings().all()

    return await create_response("success", data, "your views")


@router.get("/search", response_model=ResponseView)
async def get_specific_user_view(
    search_title: str,
    pgn: Paginator = Depends(Paginator),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> dict:
    
    query = await query_specific_user_view(user.id, search_title, pgn.limit, pgn.offset)
    result = await session.execute(text(query))
    data = result.mappings().all()
    if data == []:
        raise HTTPException(status_code=404, detail=await create_response("error", data, "not found"))

    return await create_response("success", data, "found")
