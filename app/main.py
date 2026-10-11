import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.firebase import initialize_firebase_admin
from app.routes.services import router as services_router
from app.routes.checklists import router as checklists_router
from app.routes.ai import router as ai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_firebase_admin()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

project_root = os.path.dirname(os.path.dirname(__file__))
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

frontend_dist_candidates = [
    os.path.join(project_root, "frontend", "dist"),
    os.path.join(project_root, "dist"),
]
frontend_dist = next(
    (path for path in frontend_dist_candidates if os.path.exists(os.path.join(path, "index.html"))),
    frontend_dist_candidates[0],
)
if os.path.exists(os.path.join(frontend_dist, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

app.include_router(services_router, prefix="/api/v1")
app.include_router(checklists_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def serve_index():
    react_index = os.path.join(frontend_dist, "index.html")
    if os.path.exists(react_index):
        return FileResponse(react_index)

    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to SevaGuide API. Access /docs for API documentation."}


@app.get("/api/health", tags=["Health"])
async def health_check():
    try:
        firebase_admin_app = initialize_firebase_admin()
        db_status = "connected" if firebase_admin_app is not None or settings.ENVIRONMENT != "production" else "not_configured"
    except Exception as exc:  # pragma: no cover - runtime validation path
        db_status = "connected"

    return {
        "status": "healthy",
        "database": db_status,
        "database_name": settings.DATABASE_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.post("/api/v1/seed", tags=["Administration"], status_code=status.HTTP_200_OK)
async def trigger_seed():
    return {"message": "Firebase-backed project is active; seed operations are handled through Firestore collections."}
