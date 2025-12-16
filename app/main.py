"""Точка входа в приложение."""

from fastapi import FastAPI
from .api import requirements, testcases, bugs
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import HTMLResponse

BASE_DIR = Path(__file__).parent.parent

app = FastAPI(
    title="QA helper API",
    description="Система для управления требованиями, " "тест кецсами и баг-репортами",
)

app.include_router(requirements.router)
app.include_router(testcases.router)
app.include_router(bugs.router)

STATIC_DIR = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    """Главная страница."""
    return (STATIC_DIR / "index.html").read_text(encoding="utf-8")


@app.get("/requirements", response_class=HTMLResponse)
def requirements_page():
    """Страница с требованиями."""
    return (STATIC_DIR / "requirements.html").read_text(encoding="utf-8")


@app.get("/testcases", response_class=HTMLResponse)
def testcases_page():
    """Страница с тест-кейсами."""
    return (STATIC_DIR / "testcases.html").read_text(encoding="utf-8")


@app.get("/bugs", response_class=HTMLResponse)
def bugs_page():
    """Страница с баг-репортами."""
    return (STATIC_DIR / "bugs.html").read_text(encoding="utf-8")


@app.get("/bug/{bug_id}", response_class=HTMLResponse)
def bug_detail_page(bug_id: int):
    """Страница деталей бага."""
    return (STATIC_DIR / "bug_detail.html").read_text(encoding="utf-8")


@app.get("/testcase/{testcase_id}", response_class=HTMLResponse)
def testcase_detail_page(testcase_id: int):
    """Страница деталей тест-кейса."""
    return (STATIC_DIR / "testcase_detail.html").read_text(encoding="utf-8")


@app.get("/requirement/{req_id}", response_class=HTMLResponse)
def requirement_detail_page(req_id: int):
    """Страница деталей требования."""
    return (STATIC_DIR / "requirement_detail.html").read_text(encoding="utf-8")
