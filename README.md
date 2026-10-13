# Imtiaz API

A small FastAPI project with SQLite persistence through SQLAlchemy.

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Edit `.env` to configure the application. `DATABASE_URL` defaults to `sqlite:///./app.db`; the example file uses this default. Environment variables already set in the shell take precedence over values in `.env`.

## Run

```powershell
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`; interactive documentation is at `/docs`. The SQLite database is created as `app.db` in the working directory on startup.
If the products table is empty, startup inserts five sample products. Existing product data is left unchanged.

## Endpoints

- `GET /health` checks that the application is running.
- `POST /products` creates a product (`name`, `price`, optional `category` and `stock`).
- `GET /products` lists products, including the sample products inserted at startup.
- `POST /items` creates an item.
- `GET /items` lists items.
- `GET /items/{item_id}` retrieves an item.
- `PUT /items/{item_id}` updates an item.
- `DELETE /items/{item_id}` deletes an item.

Run the tests with `pytest`.