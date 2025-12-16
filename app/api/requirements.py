"""Требования."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from ..models import Requirement
from ..database import requirements_db, save_requirements
from ..utils import export_to_csv

router = APIRouter(prefix="/requirements", tags=["requirements"])


@router.get("/", response_model=list[Requirement])
def get_requirements() -> list[Requirement]:
    """Получение требований."""
    return requirements_db


@router.post("/", response_model=Requirement)
def create_requirement(req: Requirement) -> Requirement:
    """Создание требования."""
    for r in requirements_db:
        if r.id == req.id:
            raise HTTPException(
                status_code=400, detail=f"Требование с id={req.id} уже существует"
            )
    requirements_db.append(req)
    save_requirements()
    return req


@router.get("/export.csv")
def export_requirements_csv() -> StreamingResponse:
    """Экспорт в csv."""
    headers = [
        ("id", "ID"),
        ("text", "Текст"),
        ("req_type", "Тип"),
        ("device_type", "Тип устройства"),
    ]
    return export_to_csv(requirements_db, headers, "requirements.csv")


@router.get("/{req_id}", response_model=Requirement)
def get_req(req_id: int) -> Requirement:
    """Получение требования по id."""
    for req in requirements_db:
        if req.id == req_id:
            return req
    raise HTTPException(status_code=400, detail="Требование не найдено!")


@router.delete("/{req_id}", status_code=204)
def delete_req(req_id: int):
    """Удалить требование по ID."""
    for i, req in enumerate(requirements_db):
        if req.id == req_id:
            requirements_db.pop(i)
            save_requirements()
            return
    raise HTTPException(status_code=404, detail="Требование не найдено")
