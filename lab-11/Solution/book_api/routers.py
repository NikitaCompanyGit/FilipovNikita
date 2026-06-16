from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from datetime import date, timedelta
from collections import Counter

from models import NewBookRequest, LibraryBookDto, BookChangesDto, BookLoanRequest, DetailedBookDto, Genre
from database import COLLECTION_BOOKS, COLLECTION_BORROWS, next_sequence_id, to_book_dto

router = APIRouter()

@router.get("/books", response_model=List[LibraryBookDto])
async def get_books_catalog(
    genre: Optional[Genre] = Query(None, description="Фильтрация списка по жанру"),
    author: Optional[str] = Query(None, description="Фильтрация по имени автора (вхождение подстроки)"),
    available_only: bool = Query(False, description="Показывать только свободные в наличии книги"),
    skip: int = Query(0, ge=0, description="Количество пропускаемых элементов (смещение)"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное число элементов")
):
    """
    Получение списка книг с поддержкой критериев поиска и пагинации.
    """
    results = []
    
    for book_id, item in COLLECTION_BOOKS.items():
        if genre and item["genre"] != genre:
            continue
        if author and author.lower() not in item["author"].lower():
            continue
        if available_only and not item.get("available", True):
            continue
            
        results.append(to_book_dto(book_id, item))
        
    return results[skip : skip + limit]

@router.get("/books/{book_id}", response_model=DetailedBookDto)
async def get_book_details(book_id: int):
    """
    Получение детальной информации о книге, включая статус и сроки аренды.
    """
    if book_id not in COLLECTION_BOOKS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
        
    info = COLLECTION_BOOKS[book_id]
    response = DetailedBookDto(
        id=book_id,
        title=info["title"],
        author=info["author"],
        genre=info["genre"],
        publication_year=info["publication_year"],
        pages=info["pages"],
        isbn=info["isbn"],
        available=info.get("available", True)
    )
    
    if not response.available and book_id in COLLECTION_BORROWS:
        loan = COLLECTION_BORROWS[book_id]
        response.borrowed_by = loan["borrower_name"]
        response.borrowed_date = loan["borrowed_date"]
        response.return_date = loan["return_date"]
        
    return response

@router.post("/books", response_model=LibraryBookDto, status_code=status.HTTP_201_CREATED)
async def add_book_to_catalog(book: NewBookRequest):
    """
    Добавление новой книги. Проверяет уникальность ISBN.
    """
    for item in COLLECTION_BOOKS.values():
        if item["isbn"] == book.isbn:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Книга с указанным ISBN уже зарегистрирована"
            )
            
    new_id = next_sequence_id()
    COLLECTION_BOOKS[new_id] = {
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "publication_year": book.publication_year,
        "pages": book.pages,
        "isbn": book.isbn,
        "available": True
    }
    
    return to_book_dto(new_id, COLLECTION_BOOKS[new_id])

@router.put("/books/{book_id}", response_model=LibraryBookDto)
async def edit_book_fields(book_id: int, book_update: BookChangesDto):
    """
    Редактирование свойств книги по её ID.
    """
    if book_id not in COLLECTION_BOOKS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
        
    current = COLLECTION_BOOKS[book_id]
    changes = book_update.model_dump(exclude_unset=True)
    
    if "isbn" in changes and changes["isbn"] != current["isbn"]:
        for other_id, other_book in COLLECTION_BOOKS.items():
            if other_id != book_id and other_book["isbn"] == changes["isbn"]:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Такой ISBN уже принадлежит другой книге"
                )
                
    current.update(changes)
    COLLECTION_BOOKS[book_id] = current
    
    return to_book_dto(book_id, COLLECTION_BOOKS[book_id])

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_id: int):
    """
    Удаление книги из каталога. Нельзя удалить книгу, если она на руках у читателя.
    """
    if book_id not in COLLECTION_BOOKS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
        
    if not COLLECTION_BOOKS[book_id].get("available", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить выданную книгу"
        )
        
    del COLLECTION_BOOKS[book_id]
    COLLECTION_BORROWS.pop(book_id, None)
    return None

@router.post("/books/{book_id}/borrow", response_model=DetailedBookDto)
async def loan_book_to_reader(book_id: int, req: BookLoanRequest):
    """
    Выдача книги читателю на указанный срок.
    """
    if book_id not in COLLECTION_BOOKS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
        
    if not COLLECTION_BOOKS[book_id].get("available", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Книга в данный момент выдана другому человеку"
        )
        
    COLLECTION_BOOKS[book_id]["available"] = False
    
    today = date.today()
    limit_date = today + timedelta(days=req.return_days)
    
    COLLECTION_BORROWS[book_id] = {
        "borrower_name": req.borrower_name,
        "borrowed_date": today,
        "return_date": limit_date
    }
    
    return await get_book_details(book_id)

@router.post("/books/{book_id}/return", response_model=LibraryBookDto)
async def return_loaned_book(book_id: int):
    """
    Фиксация возврата книги читателем.
    """
    if book_id not in COLLECTION_BOOKS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
        
    if COLLECTION_BOOKS[book_id].get("available", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Книга уже находится в библиотеке"
        )
        
    COLLECTION_BOOKS[book_id]["available"] = True
    COLLECTION_BORROWS.pop(book_id, None)
    
    return to_book_dto(book_id, COLLECTION_BOOKS[book_id])

@router.get("/stats")
async def calculate_catalog_statistics():
    """
    Анализ и расчет сводной статистики по библиотечному фонду.
    """
    total = len(COLLECTION_BOOKS)
    available_qty = sum(1 for b in COLLECTION_BOOKS.values() if b.get("available", True))
    borrowed_qty = total - available_qty
    
    genres = Counter(b["genre"] for b in COLLECTION_BOOKS.values())
    authors = Counter(b["author"] for b in COLLECTION_BOOKS.values())
    popular_author = authors.most_common(1)[0][0] if authors else None
    
    return {
        "total_books": total,
        "available_books": available_qty,
        "borrowed_books": borrowed_qty,
        "books_by_genre": dict(genres),
        "most_prolific_author": popular_author
    }
