from collections import OrderedDict
from uuid import UUID, uuid4

from app.models import EstadoLibro
from app.schemas import Book, BookCreate, BookPatch, BookUpdate


books_store: OrderedDict[UUID, Book] = OrderedDict()


def seed_books() -> None:
    if books_store:
        return

    initial_books = [
        BookCreate(
            titulo="Cien años de soledad",
            autor="Gabriel García Márquez",
            fechaPublicacion="1967-05-30",
            cantidad=4,
            estado=EstadoLibro.disponible,
        ),
        BookCreate(
            titulo="Rayuela",
            autor="Julio Cortázar",
            fechaPublicacion="1963-06-28",
            cantidad=2,
            estado=EstadoLibro.prestado,
        ),
        BookCreate(
            titulo="Ficciones",
            autor="Jorge Luis Borges",
            fechaPublicacion="1944-01-01",
            cantidad=5,
            estado=EstadoLibro.disponible,
        ),
    ]

    for payload in initial_books:
        create_book(payload)


def list_books() -> list[Book]:
    return list(books_store.values())


def get_book(book_id: UUID) -> Book | None:
    return books_store.get(book_id)


def create_book(payload: BookCreate) -> Book:
    book = Book(id=uuid4(), **payload.model_dump())
    books_store[book.id] = book
    return book


def replace_book(book_id: UUID, payload: BookUpdate) -> Book | None:
    if book_id not in books_store:
        return None

    book = Book(id=book_id, **payload.model_dump())
    books_store[book_id] = book
    return book


def patch_book(book_id: UUID, payload: BookPatch) -> Book | None:
    current = books_store.get(book_id)

    if current is None:
        return None

    data = current.model_dump()
    data.update(payload.model_dump(exclude_unset=True))

    updated = Book(**data)
    books_store[book_id] = updated
    return updated


def delete_book(book_id: UUID) -> bool:
    if book_id not in books_store:
        return False

    del books_store[book_id]
    return True
