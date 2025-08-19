# tests/test_api.py
# -*- coding: utf-8 -*-

from pathlib import Path

import respx
import httpx
from fastapi.testclient import TestClient

import api as api_module  # FastAPI app'i import edeceğiz
from openlibrary_client import OPENLIB_ISBN_URL, OPENLIB_AUTHOR_URL


def test_endpoints(tmp_path: Path):
    # Her test için temiz bir storage dosyası kullanalım
    storage = tmp_path / "lib.json"
    # API modülündeki global library örneğini yeniden yönlendiriyoruz.
    api_module.library._storage_path = storage  # type: ignore
    api_module.library._books = []  # type: ignore
    api_module.library.save_books()

    client = TestClient(api_module.app)

    # Başta boş olmalı
    r = client.get("/books")
    assert r.status_code == 200
    assert r.json() == []

    isbn = "9780140328721"
    with respx.mock:
        respx.get(OPENLIB_ISBN_URL.format(isbn=isbn)).mock(
            return_value=httpx.Response(
                200,
                json={"title": "Matilda", "authors": [{"key": "/authors/OL34184A"}]},
            )
        )
        respx.get(OPENLIB_AUTHOR_URL.format(key="/authors/OL34184A")).mock(
            return_value=httpx.Response(200, json={"name": "Roald Dahl"})
        )

        r = client.post("/books", json={"isbn": isbn})
        assert r.status_code == 201
        body = r.json()
        assert body["title"] == "Matilda"
        assert body["author"] == "Roald Dahl"
        assert body["isbn"] == isbn

    # GET artık 1 kitap döndürmeli
    r = client.get("/books")
    assert r.status_code == 200
    assert len(r.json()) == 1

    # DELETE başarılı
    r = client.delete(f"/books/{isbn}")
    assert r.status_code == 204

    # Tekrar silmek 404
    r = client.delete(f"/books/{isbn}")
    assert r.status_code == 404
