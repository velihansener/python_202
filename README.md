# Python 202 Bootcamp – Library Project (OOP + Open Library API + FastAPI + Frontend)

Bu repo; OOP ile terminal kütüphanesi, Open Library API ile veri zenginleştirme ve FastAPI ile REST API oluşturma adımlarını **tamamıyla** içerir. Ek olarak, API'yi tüketen basit bir **frontend** sağlanmıştır.

## Özellikler
- **Aşama 1:** `Book` ve `Library` sınıfları ile JSON kalıcılık, CLI menü.
- **Aşama 2:** ISBN girildiğinde **Open Library** API'sinden başlık ve yazar(lar)ın otomatik çekilmesi.
- **Aşama 3:** **FastAPI** ile `GET /books`, `POST /books`, `DELETE /books/{isbn}`.
- **Frontend:** Basit HTML/JS arayüz (API'ye istek atar).

## Kurulum
```bash
git clone <REPO_URL>
cd library_project
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Terminal Uygulaması (Aşama 1-2)
```bash
python main.py
```

## API (Aşama 3)
```bash
uvicorn api:app --reload
```
- Swagger UI: `http://127.0.0.1:8000/docs`

## Frontend
`frontend/index.html` dosyasını bir **static server** ile servis edin (ör. VS Code Live Server eklentisi) veya tarayıcıda açıp CORS engeline takılmamak için API'yi `http://127.0.0.1:8000`'da çalıştırın.

## Testler
```bash
pytest -q
```

## Dosya Yapısı
```
library_project/
├─ api.py
├─ library.py
├─ main.py
├─ models.py
├─ openlibrary_client.py
├─ requirements.txt
├─ tests/
│  ├─ test_library.py
│  ├─ test_openlibrary_client.py
│  └─ test_api.py
└─ frontend/
   ├─ index.html
   ├─ app.js
   └─ styles.css
```
