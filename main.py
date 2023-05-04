from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles 
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.page.template import template_router
from app.core.config import settings
from app.db.session import SessionLocal
from app.db.init_db import init_db


# Create first super user
def init() -> None:
    db = SessionLocal()
    init_db(db)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

app.mount("/static", StaticFiles(directory="static"), name="static") 
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(template_router)

init()
