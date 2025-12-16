"""База данных."""

import json
from pathlib import Path
from .models import Requirement, TestCase, BugReport

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

REQ_FILE = DATA_DIR / "requirements.json"
TC_FILE = DATA_DIR / "testcases.json"
BUG_FILE = DATA_DIR / "bug.json"


def _load_json(path: Path, model_cls):
    """Загружает список объектов из JSON-файла."""
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [model_cls(**item) for item in data]


def _save_json(path: Path, data: list):
    """Сохраняет список объектов в JSON-файл."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump([item.model_dump() for item in data], f, ensure_ascii=False, indent=2)


# Загрузка данных
requirements_db: list[Requirement] = _load_json(REQ_FILE, Requirement)
test_cases_db: list[TestCase] = _load_json(TC_FILE, TestCase)
bug_reports_db: list[BugReport] = _load_json(BUG_FILE, BugReport)


def save_requirements():
    """Сохранение требований."""
    _save_json(REQ_FILE, requirements_db)


def save_testcases():
    """Сохранение тест-кейсов."""
    _save_json(TC_FILE, test_cases_db)


def save_bugs():
    """Сохранение баг-репортов."""
    _save_json(BUG_FILE, bug_reports_db)
