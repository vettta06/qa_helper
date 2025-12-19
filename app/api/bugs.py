"""Баг-репорты."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from ..models import BugReport
from ..database import (
    get_all_bugs,
    get_bug_by_id,
    create_bug as db_create_bug,
    delete_bug as db_delete_bug,
    get_all_test_case_ids,
)
from ..utils import export_to_csv

router = APIRouter(prefix="/bugs", tags=["bugs"])


@router.get("/", response_model=list[BugReport])
def get_bugs() -> list[BugReport]:
    """Получение баг-репортов."""
    return get_all_bugs()


@router.post("/", response_model=BugReport)
def create_bug(bug: BugReport) -> BugReport:
    """Создание баг-репорта."""
    existing_test_case_ids = get_all_test_case_ids()
    if bug.test_case_id and bug.test_case_id not in existing_test_case_ids:
        raise HTTPException(
            status_code=400, detail=f"Тест-кейс с id={bug.test_case_id} не найден."
        )
    if get_bug_by_id(bug.id):
        raise HTTPException(
            status_code=400, detail=f"Баг-репорт с id={bug.id} уже существует"
        )
    return db_create_bug(bug)


@router.get("/export.csv")
def export_bugs_csv() -> StreamingResponse:
    """Экспорт в csv."""
    headers = [
        ("id", "ID"),
        ("title", "Заголовок"),
        ("severity", "Серьёзность"),
        ("environment", "Окружение"),
        ("actual_result", "Фактический результат"),
        ("expected_result", "Ожидаемый результат"),
        ("test_case_id", "ID тест-кейса"),
    ]
    return export_to_csv(get_all_bugs(), headers, "bugs.csv")


@router.get("/{bug_id}", response_model=BugReport)
def get_bug(bug_id: int) -> BugReport:
    """Получить баг-репорт по id."""
    bug = get_bug_by_id(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Баг-репорт не найден!")
    return bug


@router.delete("/{bug_id}", status_code=204)
def delete_bug(bug_id: int):
    """Удалить баг-репорт по ID."""
    if not db_delete_bug(bug_id):
        raise HTTPException(status_code=404, detail="Баг-репорт не найден")
