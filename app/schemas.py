from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models import EstadoLibro


class BookBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=150)
    autor: str = Field(..., min_length=1, max_length=120)
    fechaPublicacion: date
    cantidad: int = Field(..., ge=0)
    estado: EstadoLibro = EstadoLibro.disponible


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookPatch(BaseModel):
    titulo: Optional[str] = Field(default=None, min_length=1, max_length=150)
    autor: Optional[str] = Field(default=None, min_length=1, max_length=120)
    fechaPublicacion: Optional[date] = None
    cantidad: Optional[int] = Field(default=None, ge=0)
    estado: Optional[EstadoLibro] = None


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class PaginatedBooks(BaseModel):
    items: list[Book]
    total: int
    page: int
    size: int
    pages: int


class Stats(BaseModel):
    total: int
    disponibles: int
    prestados: int
    ultimosAgregados: list[Book]
