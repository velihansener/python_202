# tests/test_openlibrary_client.py
# -*- coding: utf-8 -*-
"""
Open Library istemcisi için ağ çağrılarını respx ile mock ediyoruz.
"""

import respx
import httpx

from openlibrary_client import OPENLIB_ISBN_URL, OPENLIB_AUTHOR_URL, fetch_book_by_isbn


@respx.mock
def test_fetch_book_by_isbn_success():
    isbn = "9780140328721"
    # 1) ISBN endpoint'i
    respx.get(OPENLIB_ISBN_URL.format(isbn=isbn)).mock(
        return_value=httpx.Response(
            200,
            json={
                "title": "Matilda",
                "authors": [{"key": "/authors/OL34184A"}],
            },
        )
    )
    # 2) Author endpoint'i
    respx.get(OPENLIB_AUTHOR_URL.format(key="/authors/OL34184A")).mock(
        return_value=httpx.Response(200, json={"name": "Roald Dahl"})
    )

    out = fetch_book_by_isbn(isbn)
    assert out is not None
    assert out["title"] == "Matilda"
    assert out["author"] == "Roald Dahl"
    assert out["isbn"] == isbn


@respx.mock
def test_fetch_book_by_isbn_not_found():
    isbn = "0000000000"
    respx.get(OPENLIB_ISBN_URL.format(isbn=isbn)).mock(
        return_value=httpx.Response(404)
    )
    assert fetch_book_by_isbn(isbn) is None
