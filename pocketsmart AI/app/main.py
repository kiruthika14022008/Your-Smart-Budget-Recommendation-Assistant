from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.database import Base, engine
from app.routes.web import router as web_router
from app.routes.auth import router as auth_router
from app.routes.planners import router as planner_router


BASE_DIR = Path(__file__).resolve().parent

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="PocketSmart AI - Smart Budget and Recommendation Assistant",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------

app.include_router(web_router)
app.include_router(auth_router, prefix="/api")
app.include_router(planner_router, prefix="/api")


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "application": settings.APP_NAME,
        "ai_enabled": settings.gemini_enabled,
    }


# ---------------------------------------------------------
# Startup
# ---------------------------------------------------------

@app.on_event("startup")
def startup():

    upload_directory = BASE_DIR / "uploads"

    upload_directory.mkdir(
        parents=True,
        exist_ok=True,
    )