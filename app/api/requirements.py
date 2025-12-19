"""Требования."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from ..models import Requirement
from ..database import (
    get_all_requirements,
    get_requirement_by_id,
    create_requirement as db_create_requirement,
    delete_requirement as db_delete_requirement,
)
from ..utils import export_to_csv

router = APIRouter(prefix="/requirements", tags=["requirements"])


@router.get("/", response_model=list[Requirement])
def get_requirements() -> list[Requirement]:
    """Получение требований."""
    return get_all_requirements()


@router.post("/", response_model=Requirement)
def create_requirement(req: Requirement) -> Requirement:
    """Создание требования."""
    if get_requirement_by_id(req.id):
        raise HTTPException(
            status_code=400, detail=f"Требование с id={req.id} уже существует"
        )
    return db_create_requirement(req)


@router.get("/export.csv")
def export_requirements_csv() -> StreamingResponse:
    """Экспорт в csv."""
    headers = [
        ("id", "ID"),
        ("text", "Текст"),
        ("req_type", "Тип"),
        ("device_type", "Тип устройства"),
    ]
    return export_to_csv(get_all_requirements(), headers, "requirements.csv")


@router.get("/{req_id}", response_model=Requirement)
def get_req(req_id: int) -> Requirement:
    """Получение требования по id."""
    req = get_requirement_by_id(req_id)
    if not req:
        raise HTTPException(status_code=404, detail="Требование не найдено!")
    return req


@router.delete("/{req_id}", status_code=204)
def delete_req(req_id: int):
    """Удалить требование по ID."""
    if not db_delete_requirement(req_id):
        raise HTTPException(status_code=404, detail="Требование не найдено")
