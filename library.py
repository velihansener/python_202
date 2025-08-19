# library.py
# -*- coding: utf-8 -*-
"""
Library sınıfı: kitap ekleme, silme, arama, listeleme ve kalıcı hale getirme (JSON).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from models import Book


class Library:
    """Kütüphane operasyonlarını yöneten sınıf."""

    def __init__(self, storage_file: str = "library.json") -> None:
        # Kitapları bellekte tutacağımız liste
        self._books: List[Book] = []
        # Verilerin kalıcı tutulacağı JSON dosyası
        self._storage_path = Path(storage_file)
        # Uygulama başlarken diskte kayıtlı kitapları yükle
        self.load_books()

    # ----------------- Kalıcılık (Persistence) -----------------

    def load_books(self) -> None:
        """JSON dosyasından kitapları yükler. Dosya yoksa sessizce geçer."""
        if not self._storage_path.exists():
            # Dosya yoksa ilk kullanım olabilir; hata fırlatmayalım.
            self._books = []
            return
        try:
            data = json.loads(self._storage_path.read_text(encoding="utf-8"))
            self._books = [Book(**item) for item in data]
        except json.JSONDecodeError:
            # Bozuk bir dosya senaryosunda veri kaybını engellemek için boş liste ile devam.
            self._books = []

    def save_books(self) -> None:
        """Mevcut kitap listesini JSON dosyasına yazar."""
        as_dicts = [dict(title=b.title, author=b.author, isbn=b.isbn) for b in self._books]
        self._storage_path.write_text(json.dumps(as_dicts, ensure_ascii=False, indent=2), encoding="utf-8")

    # ----------------- CRUD Operasyonları -----------------

    def add_book(self, book: Book) -> None:
        """Yeni bir kitabı kütüphaneye ekler. ISBN benzersiz olmalıdır.

        Args:
            book (Book): Eklenecek kitap nesnesi.

        Raises:
            ValueError: Aynı ISBN'e sahip bir kitap zaten varsa.
        """
        if self.find_book(book.isbn):
            raise ValueError(f"ISBN zaten mevcut: {book.isbn}")
        self._books.append(book)
        self.save_books()

    def remove_book(self, isbn: str) -> bool:
        """ISBN'e göre kitabı siler.

        Returns:
            bool: Silme başarılıysa True, kitap bulunamazsa False.
        """
        for idx, bk in enumerate(self._books):
            if bk.isbn == isbn:
                del self._books[idx]
                self.save_books()
                return True
        return False

    def list_books(self) -> List[Book]:
        """Tüm kitapları döndürür."""
        return list(self._books)

    def find_book(self, isbn: str) -> Optional[Book]:
        """ISBN'e göre kitabı arar ve döndürür."""
        return next((b for b in self._books if b.isbn == isbn), None)
