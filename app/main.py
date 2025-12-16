"""Точка входа в приложение."""
from fastapi import FastAPI
from .api import requirements, testcases, bugs

app = FastAPI(
    title="QA helper API",
    description="Система для управления требованиями, "
    "тест кецсами и баг-репортами"
)

app.include_router(requirements.router)
app.include_router(testcases.router)
app.include_router(bugs.router)
