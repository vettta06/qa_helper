"""Требования."""
from fastapi import APIRouter
from ..models import Requirement
from ..database import requirements_db

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
            raise ValueError(f"Требование с id={req.id} уже существует")
    requirements_db.append(req)
    return req
