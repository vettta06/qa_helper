"""Тест-кейсы."""

from fastapi import APIRouter, HTTPException
from ..models import TestCase
from ..database import (
    get_all_testcases,
    get_testcase_by_id,
    create_testcase as db_create_testcase,
    delete_testcase as db_delete_testcase,
    get_all_requirement_ids,
)
from ..utils import export_to_csv

router = APIRouter(prefix="/testcases", tags=["testcases"])


@router.get("/", response_model=list[TestCase])
def get_testcases() -> list[TestCase]:
    """Получение тест-кейсов."""
    return get_all_testcases()


@router.post("/", response_model=TestCase)
def create_testcase(testcase: TestCase) -> TestCase:
    """Создание тест-кейса."""
    if get_testcase_by_id(testcase.id):
        raise HTTPException(
            status_code=400, detail=f"Тест-кейс с id={testcase.id} уже существует"
        )
    requirement_ids = get_all_requirement_ids()
    if testcase.requirement_id not in requirement_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Требование с id={testcase.requirement_id} не найдено. "
            f"Допустимые id: {sorted(requirement_ids)}",
        )
    return db_create_testcase(testcase)


@router.get("/export.csv")
def export_testcases_csv():
    """Экспорт в csv."""
    headers = [
        ("id", "ID"),
        ("requirement_id", "ID требования"),
        ("description", "Описание"),
        ("steps", "Шаги"),
        ("expected_result", "Ожидаемый результат"),
    ]
    data = [
        {**tc.model_dump(), "steps": "; ".join(tc.steps)} for tc in get_all_testcases()
    ]
    return export_to_csv(data, headers, "testcases.csv")


@router.get("/{testcase_id}", response_model=TestCase)
def get_testcase(testcase_id: int) -> TestCase:
    """Получение тест-кейса по id."""
    tc = get_testcase_by_id(testcase_id)
    if not tc:
        raise HTTPException(status_code=404, detail="Тест-кейс не найден!")
    return tc


@router.delete("/{testcase_id}", status_code=204)
def delete_testcase(testcase_id: int):
    """Удалить тест-кейс по ID."""
    if not db_delete_testcase(testcase_id):
        raise HTTPException(status_code=404, detail="Тест-кейс не найден")
