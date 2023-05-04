from fastapi import APIRouter

from app.page import pages

template_router = APIRouter()
template_router.include_router(pages.router)
