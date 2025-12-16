"""Модели данных."""
from pydantic import BaseModel
from enum import Enum


class Severity(str, Enum):
    """Уровни важности проблемы."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Requirement(BaseModel):
    """Требования к устройству."""
    id: int
    text: str
    req_type: str  # functional or nonfunctional


class TestCase(BaseModel):
    """Тестовые кейсы."""
    id: int
    requirement_id: int
    description: str
    steps: list[str]
    expected_res: str


class BugReport(BaseModel):
    """Создание репортов."""
    id: int
    title: str
    severity: Severity
    steps_to_reduce: list[str]
    actual_res: str
    expected_res: str
    environment: str
    test_case_id: int | None = None
