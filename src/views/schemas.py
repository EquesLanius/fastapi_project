from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class NewView(BaseModel):
    title: str
    view_date: date
    season: Optional[int] = None
    episode: Optional[int] = None


class HistoryView(BaseModel):
    title: str
    release_year: int
    view_date: date
    is_series: str
    season: Optional[int] = None
    episode: Optional[int] = None


class CatalogRecord(BaseModel):
    title: str
    release_year: int
    is_series: Optional[bool] = False


class ResponseCatalog(BaseModel):
    status: str
    data: List[CatalogRecord]
    details: str


class ResponseView(BaseModel):
    status: str
    data: List[HistoryView]
    details: str


class ResponseAddView(BaseModel):
    status: str
    data: NewView
    details: str