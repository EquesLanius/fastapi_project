from datetime import date



async def query_exist_cat(title: str, year: date, is_series: bool) -> str:

    query = (
        f"INSERT INTO catalog (title, release_year, is_series) "\
        f"SELECT '{title}', {year}, {is_series} "\
        f"WHERE NOT EXISTS ( "\
        f"SELECT title, release_year, is_series FROM catalog "\
        f"WHERE title = '{title}' AND release_year = {year} AND is_series = {is_series}) "\
        f"RETURNING id"
    )

    return query


async def query_exist_view(uid: int, cid: int, vdate: date, season: int, episode: int) -> str:

    query = (
        f"INSERT INTO view (user_id, catalog_id, view_date, season, episode) "\
        f"SELECT {uid}, {cid}, '{vdate}', {season}, {episode} "\
        f"WHERE NOT EXISTS ( "\
        f"SELECT catalog_id, view_date, season, episode FROM view "\
        f"WHERE catalog_id = {cid} AND view_date = '{vdate}' AND "\
        f"(CASE WHEN {season} != 0 THEN season ELSE 0 END) = {season} AND "\
        f"(CASE WHEN {episode} != 0 THEN episode ELSE 0 END) = {episode}) "\
        f"RETURNING id"
    )

    return query


async def query_user_views(uid: int, limit: int, offset: int) -> str:
    
    query = (
        f"SELECT catalog.title, catalog.release_year, view.view_date, "\
        f"CASE catalog.is_series WHEN false THEN 'Movie' WHEN true THEN 'Series' "\
        f"END is_series, view.season, view.episode "\
        f"FROM view JOIN catalog ON catalog.id = view.catalog_id "\
        f"WHERE view.user_id = {uid} ORDER BY view.view_date LIMIT {limit} OFFSET {offset}"
    )

    return query


async def query_specific_user_view(uid: int, title: str, limit: int, offset: int) -> str:
    
    query = (
        f"SELECT catalog.title, catalog.release_year, view.view_date, "\
        f"CASE catalog.is_series WHEN false THEN 'Movie' WHEN true THEN 'Series' "\
        f"END is_series, view.season, view.episode "\
        f"FROM view JOIN catalog ON catalog.id = view.catalog_id "\
        f"WHERE view.user_id = {uid} AND catalog.title = '{title}' ORDER BY view.view_date LIMIT {limit} OFFSET {offset}"
    )

    return query
