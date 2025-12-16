"""Баг-репорты."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from ..models import BugReport
from ..database import bug_reports_db, test_cases_db, save_bugs
from ..utils import export_to_csv

router = APIRouter(prefix="/bugs", tags=["bugs"])


@router.get("/", response_model=list[BugReport])
def get_bugs() -> list[BugReport]:
    """Получение баг-репортов."""
    return bug_reports_db


@router.post("/", response_model=BugReport)
def create_bug(bug: BugReport) -> BugReport:
    """Создание баг-репорта."""
    existing_test_case_ids = {tc.id for tc in test_cases_db}
    if bug.test_case_id:
        if bug.test_case_id not in existing_test_case_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Тест-кейс с id={bug.test_case_id} не найден."
            )
    for b in bug_reports_db:
        if b.id == bug.id:
            raise HTTPException(
                status_code=400,
                detail=f"Баг-репорт с id={bug.id} уже существует"
            )
    bug_reports_db.append(bug)
    save_bugs()
    return bug


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
        ("test_case_id", "ID тест-кейса")
    ]
    return export_to_csv(bug_reports_db, headers, "bugs.csv")


@router.get("/{bug_id}", response_model=BugReport)
def get_bug(bug_id: int) -> BugReport:
    """Получить баг-репорт по id."""
    for bug in bug_reports_db:
        if bug.id == bug_id:
            return bug
    raise HTTPException(status_code=400, detail="Баг-репорт не найден!")


@router.delete("/{bug_id}", status_code=204)
def delete_bug(bug_id: int):
    """Удалить баг-репорт по ID."""
    for i, bug in enumerate(bug_reports_db):
        if bug.id == bug_id:
            bug_reports_db.pop(i)
            save_bugs()
            return
    raise HTTPException(status_code=404, detail="Баг-репорт не найден")
