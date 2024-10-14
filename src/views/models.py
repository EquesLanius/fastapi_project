from sqlalchemy import Integer, String, Table, Column, ForeignKey, Date, Boolean
from auth.models import user
#from src.auth.models import User

from database import metadata


catalog = Table(
    "catalog",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("release_year", Integer, nullable=False),
    Column("is_series", Boolean, default=False, nullable=True),
)


view = Table(
    "view",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(user.c.id)),
    Column("catalog_id", Integer, ForeignKey(catalog.c.id)),
    Column("view_date", Date, nullable=False),
    Column("season", Integer, nullable=True),
    Column("episode", Integer, nullable=True),
)
