# models.py
# -*- coding: utf-8 -*-
"""
Domain modelleri.
Bu dosya, bir kitabı temsil eden Book sınıfını içerir.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Book:
    """Kütüphanedeki bir kitabı temsil eder.

    Attributes:
        title (str): Kitabın başlığı.
        author (str): Kitabın yazarı (veya yazarlar virgülle ayrılmış).
        isbn (str): Kitabın benzersiz ISBN numarası.
    """
    title: str
    author: str
    isbn: str

    def __str__(self) -> str:
        # __str__ override: insan-okur dostu bir temsil döndürür.
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
