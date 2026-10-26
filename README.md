# Northstar Goods

A small ecommerce storefront with a Flask and SQLite API and a Next.js frontend.

## Run with Docker

From the repository root, build and start both services:

```powershell
docker compose up --build -d
```

The frontend is at <http://localhost:3000>; the backend API is at <http://localhost:8000>. SQLite data is persisted in the `sqlite_data` named volume.

Useful commands:

```powershell
# Follow logs
docker compose logs -f

# Stop the services without removing the database volume
docker compose stop

# Rebuild and start after code or configuration changes
docker compose up --build -d
```

Verify the backend from PowerShell:

```powershell
curl.exe http://localhost:8000/health
curl.exe http://localhost:8000/api/products
```

Then open <http://localhost:3000> in a browser. The frontend talks directly to the backend using `NEXT_PUBLIC_API_URL`; browser access is allowed by the configured `FRONTEND_ORIGIN`. Server-side frontend requests use `BACKEND_API_URL` on the Docker network.

The service variables are listed in [backend/.env.example](backend/.env.example) and [frontend/.env.example](frontend/.env.example). Compose has matching defaults; to override them, create a root `.env` file with `DATABASE_PATH`, `FRONTEND_ORIGIN`, `NEXT_PUBLIC_API_URL`, and/or `BACKEND_API_URL`. The public API URL is a build argument, so rebuild the frontend after changing it.

## Run locally without Docker

The backend app is Flask (not FastAPI) and defaults to a local `products.db`. See [backend/README.md](backend/README.md) for API details. Start the backend from `backend`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:FRONTEND_ORIGIN = "http://localhost:3000"
$env:DATABASE_PATH = "products.db"
python -m flask --app app run --host 0.0.0.0 --port 8000
```

In a second terminal, set the frontend API URL and start Next.js:

```powershell
Set-Location frontend
npm ci
Copy-Item .env.example .env.local
$env:NEXT_PUBLIC_API_URL = "http://localhost:8000"
$env:BACKEND_API_URL = "http://localhost:8000"
npm run dev
```

## Tests

Run the backend suite from `backend`:

```powershell
python -m unittest discover -s tests -v
```

Run the frontend configuration tests from `frontend`:

```powershell
node --test tests/config.test.mjs
```

The frontend route checks also run with `npm test` when the frontend server is available.
