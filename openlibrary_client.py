# openlibrary_client.py
# -*- coding: utf-8 -*-
"""
Open Library Books API istemcisi.
Aşama 2 gereği: ISBN ile başlık ve yazar(lar)ı otomatik çekme.
"""

import httpx
from typing import Optional


OPENLIB_ISBN_URL = "https://openlibrary.org/isbn/{isbn}.json"
OPENLIB_AUTHOR_URL = "https://openlibrary.org{key}.json"  # author key: "/authors/OL...A"


def fetch_book_by_isbn(isbn: str, timeout: float = 10.0) -> Optional[dict]:
    """ISBN'e göre Open Library'den kitap bilgisi çeker.

    Returns:
        Optional[dict]: {"title": str, "author": str, "isbn": str} sözlüğü ya da None.
    """
    isbn = isbn.strip()
    if not isbn:
        return None

    try:
        # 1) ISBN datasını çek
        with httpx.Client(timeout=timeout) as client:
            r = client.get(OPENLIB_ISBN_URL.format(isbn=isbn))
            if r.status_code != 200:
                return None
            data = r.json()
            title = data.get("title", "").strip()
            authors = data.get("authors", [])  # genelde [{"key": "/authors/OL..A"}, ...]

            # 2) Yazar isimlerini çek (varsa)
            names = []
            for a in authors:
                key = a.get("key")
                if not key:
                    continue
                ar = client.get(OPENLIB_AUTHOR_URL.format(key=key))
                if ar.status_code == 200:
                    aname = ar.json().get("name")
                    if aname:
                        names.append(aname)

            author = ", ".join(names) if names else "Unknown"
            if not title:
                return None

            return {"title": title, "author": author, "isbn": isbn}
    except Exception:
        # İnternet yok, zaman aşımı vb. durumlarda None döndür.
        return None
