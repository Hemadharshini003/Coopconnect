import sys
import os

# Ensure backend root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.db.session import engine, Base
from app.db.models import *  # Ensure all models are imported before metadata creation
from app.schemas.response import error_response

# Import all API v1 routers
from app.api.v1.auth import router as auth_router
from app.api.v1.cooperatives import router as cooperatives_router
from app.api.v1.members import router as members_router
from app.api.v1.skills import router as skills_router
from app.api.v1.assessments import router as assessments_router
from app.api.v1.courses import router as courses_router
from app.api.v1.quizzes import router as quizzes_router
from app.api.v1.opportunities import router as opportunities_router
from app.api.v1.applications import router as applications_router
from app.api.v1.placements import router as placements_router
from app.api.v1.dashboards import router as dashboards_router
from app.api.v1.sync import router as sync_router
from app.api.v1.integrations import router as integrations_router
from app.api.v1.ai import router as ai_router
from app.api.v1.districts import router as districts_router
from app.api.v1.employees import router as employees_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.hq import router as hq_router

# Auto-create tables for development / SQLite fallback
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="COOPCONNECT - Backend API",
    description="AI-Enabled Training Intelligence & Outcome Platform across 20 Institutes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger("uvicorn.error")

# Custom exception handler for safe error formatting
@app.exception_handler(Exception)
async def custom_global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None)
        )
    logger.error(f"Unhandled Exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=error_response(
            code="INTERNAL_SERVER_ERROR",
            message=str(exc) if settings.APP_ENV == "development" else "An unexpected server error occurred."
        )
    )

# Include API v1 Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(cooperatives_router, prefix=settings.API_V1_STR)
app.include_router(members_router, prefix=settings.API_V1_STR)
app.include_router(skills_router, prefix=settings.API_V1_STR)
app.include_router(assessments_router, prefix=settings.API_V1_STR)
app.include_router(courses_router, prefix=settings.API_V1_STR)
app.include_router(quizzes_router, prefix=settings.API_V1_STR)
app.include_router(opportunities_router, prefix=settings.API_V1_STR)
app.include_router(applications_router, prefix=settings.API_V1_STR)
app.include_router(placements_router, prefix=settings.API_V1_STR)
app.include_router(dashboards_router, prefix=settings.API_V1_STR)
app.include_router(sync_router, prefix=settings.API_V1_STR)
app.include_router(integrations_router, prefix=settings.API_V1_STR)
app.include_router(ai_router, prefix=settings.API_V1_STR)
app.include_router(districts_router, prefix=settings.API_V1_STR)
app.include_router(employees_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)
app.include_router(hq_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "service": "COOPCONNECT API",
        "status": "Operational",
        "documentation": "/docs"
    }

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)
