"""Требования."""
from fastapi import APIRouter, HTTPException
from ..models import Requirement
from ..database import requirements_db, save_requirements

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
                status_code=400,
                detail=f"Требование с id={req.id} уже существует"
                )
    requirements_db.append(req)
    save_requirements()
    return req
