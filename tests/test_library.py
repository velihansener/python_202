# tests/test_library.py
# -*- coding: utf-8 -*-

import json
from pathlib import Path

import pytest

from models import Book
from library import Library


def test_add_and_find_and_remove(tmp_path: Path):
    storage = tmp_path / "lib.json"
    lib = Library(str(storage))

    b = Book(title="Test", author="Author", isbn="123")
    lib.add_book(b)

    assert lib.find_book("123").title == "Test"
    assert len(lib.list_books()) == 1

    # Aynı ISBN tekrar eklenemez
    with pytest.raises(ValueError):
        lib.add_book(b)

    assert lib.remove_book("123") is True
    assert lib.find_book("123") is None
    assert lib.remove_book("123") is False  # zaten yok

    # JSON kalıcılık testi
    lib.add_book(Book("T1", "A1", "111"))
    lib2 = Library(str(storage))
    assert lib2.find_book("111") is not None
