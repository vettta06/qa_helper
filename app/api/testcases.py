"""Тест-кейсы."""
from fastapi import APIRouter
from ..models import TestCase
from ..database import test_cases_db, requirements_db

router = APIRouter(prefix="/testcases", tags=["testcases"])


@router.get("/", response_model=list[TestCase])
def get_testcases() -> list[TestCase]:
    """Получение тест-кейсов."""
    return test_cases_db


@router.post("/", response_model=TestCase)
def create_testcase(testcase: TestCase) -> TestCase:
    """Создание тест-кейса."""
    for test in test_cases_db:
        if test.id == testcase.id:
            raise ValueError(f"Требование с id={test.id} уже существует")
        
    requirement_ids = {r.id for r in requirements_db}
    if testcase.requirement_id not in requirement_ids:
        raise ValueError(
            f"Требование с id={testcase.requirement_id} не найдено. "
            f"Допустимые id: {sorted(requirement_ids)}"
        )
    test_cases_db.append(testcase)
    return testcase
