# SevaGuide

SevaGuide provides a React/Vite citizen portal and a FastAPI backend for guidance on Indian government certificate applications.

## Requirements

- Python 3.10+
- Node.js 20.19+ or 22.12+

## Run the backend

From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

The API documentation is available at `http://127.0.0.1:8000/docs` and the health endpoint at `http://127.0.0.1:8000/api/health`. Firebase Admin and Gemini credentials are optional for local development; configure them in `.env` to enable those integrations. Do not commit `.env`.

## Run the frontend

In a second terminal:

```powershell
npm ci
npm run dev
```

The Vite development server runs at `http://localhost:3000` and proxies API requests to the backend. To build the frontend for the backend to serve:

```powershell
npm run build
```

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```
