# api.py
# -*- coding: utf-8 -*-
"""
FastAPI uygulaması (Aşama 3).
Endpoint'ler:
- GET    /books          -> tüm kitaplar
- POST   /books          -> ISBN alır, Open Library'den çekip ekler
- DELETE /books/{isbn}   -> kitabı siler
"""

from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from models import Book
from library import Library
from openlibrary_client import fetch_book_by_isbn

app = FastAPI(title="Library API", version="1.0.0")
library = Library("library.json")  # Tek bir paylaşılan Library örneği

# --------------- Pydantic Modelleri ---------------

class BookModel(BaseModel):
    title: str
    author: str
    isbn: str

    @staticmethod
    def from_book(b: Book) -> "BookModel":
        return BookModel(title=b.title, author=b.author, isbn=b.isbn)


class ISBNRequest(BaseModel):
    isbn: str = Field(..., description="Kitabın ISBN numarası")


# --------------- Endpoint'ler ---------------

@app.get("/books", response_model=List[BookModel])
def get_books():
    """Kütüphanedeki tüm kitapları döndürür."""
    return [BookModel.from_book(b) for b in library.list_books()]


@app.post("/books", response_model=BookModel, status_code=201)
def create_book(payload: ISBNRequest):
    """ISBN'e göre Open Library'den veriyi çekip kitabı ekler."""
    info = fetch_book_by_isbn(payload.isbn)
    if not info:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı veya ağ hatası.")

    book = Book(title=info["title"], author=info["author"], isbn=info["isbn"])
    try:
        library.add_book(book)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return BookModel.from_book(book)


@app.delete("/books/{isbn}", status_code=204)
def delete_book(isbn: str):
    """ISBN'e göre kitabı siler."""
    ok = library.remove_book(isbn)
    if not ok:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    return
