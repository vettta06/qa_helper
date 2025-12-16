"""Тест-кейсы."""
from fastapi import APIRouter, HTTPException
from ..models import TestCase
from ..database import test_cases_db, requirements_db, save_testcases

router = APIRouter(prefix="/testcases", tags=["testcases"])


@router.get("/", response_model=list[TestCase])
def get_testcases() -> list[TestCase]:
    """Получение тест-кейсов."""
    return test_cases_db


@router.post("/", response_model=TestCase)
def create_testcase(testcase: TestCase) -> TestCase:
    """Создание тест-кейса."""
    if any(tc.id == testcase.id for tc in test_cases_db):
        raise HTTPException(
            status_code=400,
            detail=f"Тест-кейс с id={testcase.id} уже существует"
        )
    requirement_ids = {r.id for r in requirements_db}
    if testcase.requirement_id not in requirement_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Требование с id={testcase.requirement_id} не найдено. "
            f"Допустимые id: {sorted(requirement_ids)}"
        )
    test_cases_db.append(testcase)
    save_testcases()
    return testcase


@router.get("/{testcase_id}", response_model=TestCase)
def get_testcase(testcase_id: int) -> TestCase:
    """Получение тест-кейса по id."""
    for test in test_cases_db:
        if test.id == testcase_id:
            return test
    raise HTTPException(status_code=400, detail="Тест-кейс не найден!")
