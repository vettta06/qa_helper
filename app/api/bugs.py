"""Баг-репорты."""
from fastapi import APIRouter, HTTPException
from ..models import BugReport
from ..database import bug_reports_db, test_cases_db, save_bugs

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
