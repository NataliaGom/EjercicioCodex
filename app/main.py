from contextlib import asynccontextmanager
from math import ceil
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.models import EstadoLibro
from app.schemas import Book, BookCreate, BookPatch, BookUpdate, PaginatedBooks, Stats
from app.store import (
    create_book,
    delete_book,
    get_book,
    list_books,
    patch_book,
    replace_book,
    seed_books,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_books()
    yield


app = FastAPI(
    title="Biblioteca API",
    version="1.0.0",
    description="API en FastAPI para gestionar libros de una biblioteca sin base de datos.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aguayo-0107.github.io",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/books", response_model=PaginatedBooks)
def read_books(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    q: str | None = None,
    titulo: str | None = None,
    autor: str | None = None,
    estado: EstadoLibro | None = None,
    sort: str = Query(
        default="titulo_asc",
        pattern="^(titulo_asc|titulo_desc|fecha_asc|fecha_desc)$",
    ),
):
    books = list_books()

    if q:
        value = q.lower()
        books = [
            book
            for book in books
            if value in book.titulo.lower() or value in book.autor.lower()
        ]

    if titulo:
        value = titulo.lower()
        books = [book for book in books if value in book.titulo.lower()]

    if autor:
        value = autor.lower()
        books = [book for book in books if value in book.autor.lower()]

    if estado:
        books = [book for book in books if book.estado == estado]

    if sort == "titulo_asc":
        books.sort(key=lambda book: book.titulo.lower())
    elif sort == "titulo_desc":
        books.sort(key=lambda book: book.titulo.lower(), reverse=True)
    elif sort == "fecha_asc":
        books.sort(key=lambda book: book.fechaPublicacion)
    elif sort == "fecha_desc":
        books.sort(key=lambda book: book.fechaPublicacion, reverse=True)

    total = len(books)
    start = (page - 1) * size
    end = start + size
    items = books[start:end]

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": ceil(total / size) if total else 0,
    }


@app.get("/books/status/{estado}", response_model=list[Book])
def read_books_by_status(estado: EstadoLibro):
    return [book for book in list_books() if book.estado == estado]


@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: UUID):
    book = get_book(book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return book


@app.post("/books", response_model=Book, status_code=201)
def create_book_endpoint(payload: BookCreate):
    return create_book(payload)


@app.put("/books/{book_id}", response_model=Book)
def update_book_endpoint(book_id: UUID, payload: BookUpdate):
    book = replace_book(book_id, payload)

    if book is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return book


@app.patch("/books/{book_id}", response_model=Book)
def patch_book_endpoint(book_id: UUID, payload: BookPatch):
    book = patch_book(book_id, payload)

    if book is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return book


@app.delete("/books/{book_id}")
def delete_book_endpoint(book_id: UUID):
    deleted = delete_book(book_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return {"message": "Libro eliminado correctamente"}


@app.get("/stats", response_model=Stats)
def stats():
    books = list_books()

    disponibles = [book for book in books if book.estado == EstadoLibro.disponible]
    prestados = [book for book in books if book.estado == EstadoLibro.prestado]

    return {
        "total": len(books),
        "disponibles": len(disponibles),
        "prestados": len(prestados),
        "ultimosAgregados": books[-5:][::-1],
    }
