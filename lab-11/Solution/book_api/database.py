from typing import Dict
from models import LibraryBookDto

# Локальное хранилище данных (in-memory)
COLLECTION_BOOKS: Dict[int, dict] = {}
COLLECTION_BORROWS: Dict[int, dict] = {}
_id_seq_generator = 1

def next_sequence_id() -> int:
    """Генерация автоинкрементного ключа для новой книги"""
    global _id_seq_generator
    uid = _id_seq_generator
    _id_seq_generator += 1
    return uid

def to_book_dto(book_id: int, data: dict) -> LibraryBookDto:
    """Маппинг данных словаря в DTO ответа"""
    return LibraryBookDto(
        id=book_id,
        title=data["title"],
        author=data["author"],
        genre=data["genre"],
        publication_year=data["publication_year"],
        pages=data["pages"],
        isbn=data["isbn"],
        available=data.get("available", True)
    )
