"""Точка входа в приложение."""
from fastapi import FastAPI
from .api import requirements, testcases, bugs
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import HTMLResponse

BASE_DIR = Path(__file__).parent.parent

app = FastAPI(
    title="QA helper API",
    description="Система для управления требованиями, "
    "тест кецсами и баг-репортами"
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(requirements.router)
app.include_router(testcases.router)
app.include_router(bugs.router)

STATIC_DIR = Path(__file__).parent.parent / "static"

