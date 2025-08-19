# main.py
# -*- coding: utf-8 -*-
"""
Terminal arayüzü (Aşama 1 & 2).
- Kitap ekle (ISBN ile Open Library'den otomatik doldurma)
- Sil, Listele, Ara
"""

from models import Book
from library import Library
from openlibrary_client import fetch_book_by_isbn


def print_menu() -> None:
    print("\n=== Kütüphane Uygulaması ===")
    print("1. Kitap Ekle (ISBN ile)")
    print("2. Kitap Sil")
    print("3. Kitapları Listele")
    print("4. Kitap Ara (ISBN)")
    print("5. Çıkış")


def add_book_flow(lib: Library) -> None:
    isbn = input("ISBN girin: ").strip()
    info = fetch_book_by_isbn(isbn)
    if not info:
        print("❌ Kitap bulunamadı veya ağ hatası.")
        return
    book = Book(title=info["title"], author=info["author"], isbn=info["isbn"])
    try:
        lib.add_book(book)
        print(f"✅ Eklendi: {book}")
    except ValueError as e:
        print(f"❗ {e}")


def remove_book_flow(lib: Library) -> None:
    isbn = input("Silinecek ISBN: ").strip()
    ok = lib.remove_book(isbn)
    print("✅ Silindi" if ok else "❌ Kitap bulunamadı")


def list_books_flow(lib: Library) -> None:
    books = lib.list_books()
    if not books:
        print("(Henüz kitap yok)")
        return
    for b in books:
        print("-", b)


def find_book_flow(lib: Library) -> None:
    isbn = input("Aranacak ISBN: ").strip()
    book = lib.find_book(isbn)
    print(book if book else "❌ Bulunamadı")


def main() -> None:
    lib = Library("library.json")
    while True:
        print_menu()
        choice = input("Seçim: ").strip()
        if choice == "1":
            add_book_flow(lib)
        elif choice == "2":
            remove_book_flow(lib)
        elif choice == "3":
            list_books_flow(lib)
        elif choice == "4":
            find_book_flow(lib)
        elif choice == "5":
            print("Güle güle!")
            break
        else:
            print("Geçersiz seçim.")


if __name__ == "__main__":
    main()
