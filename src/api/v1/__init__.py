"""API v1 router setup."""

from fastapi import APIRouter

from src.api.v1.library import router as library_router


api_router = APIRouter()
api_router.include_router(library_router, tags=["library"])
