"""База данных."""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from .models import Requirement, BugReport, TestCase

SQLALCHEMY_DATABASE_URL = "postgresql://qa_user:qa_pass@localhost/qa_helper"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_all_bugs() -> List[BugReport]:
    with SessionLocal() as session:
        result = session.execute(
            text(
                """
            SELECT id, title, severity, steps_to_reproduce, actual_result,
                   expected_result, environment, test_case_id
            FROM bug_reports
        """
            )
        )
        return [BugReport(**row._asdict()) for row in result]


def get_bug_by_id(bug_id: int) -> Optional[BugReport]:
    with SessionLocal() as session:
        result = session.execute(
            text(
                """
            SELECT id, title, severity, steps_to_reproduce, actual_result,
                   expected_result, environment, test_case_id
            FROM bug_reports
            WHERE id = :bug_id
        """
            ),
            {"bug_id": bug_id},
        )
        row = result.fetchone()
        return BugReport(**row._asdict()) if row else None


def create_bug(bug: BugReport) -> BugReport:
    with SessionLocal() as session:
        session.execute(
            text(
                """
            INSERT INTO bug_reports
            (id, title, severity, steps_to_reproduce, actual_result, expected_result, environment, test_case_id)
            VALUES (:id, :title, :severity, :steps_to_reproduce, :actual_result, :expected_result, :environment, :test_case_id)
        """
            ),
            {
                "id": bug.id,
                "title": bug.title,
                "severity": bug.severity,
                "steps_to_reproduce": bug.steps_to_reproduce,
                "actual_result": bug.actual_result,
                "expected_result": bug.expected_result,
                "environment": bug.environment,
                "test_case_id": bug.test_case_id,
            },
        )
        session.commit()
        return bug


def delete_bug(bug_id: int) -> bool:
    with SessionLocal() as session:
        result = session.execute(
            text(
                """
            DELETE FROM bug_reports WHERE id = :bug_id
        """
            ),
            {"bug_id": bug_id},
        )
        session.commit()
        return result.rowcount > 0


def get_all_test_case_ids() -> set[int]:
    with SessionLocal() as session:
        result = session.execute(text("SELECT id FROM test_cases"))
        return {row.id for row in result}


def get_all_requirements() -> List[Requirement]:
    with SessionLocal() as session:
        result = session.execute(
            text(
                """
            SELECT id, text, req_type, device_type FROM requirements
        """
            )
        )
        return [Requirement(**row._asdict()) for row in result]


def get_requirement_by_id(req_id: int) -> Optional[Requirement]:
    with SessionLocal() as session:
        result = session.execute(
            text(
                """
            SELECT id, text, req_type, device_type FROM requirements
            WHERE id = :req_id
        """
            ),
            {"req_id": req_id},
        )
        row = result.fetchone()
        return Requirement(**row._asdict()) if row else None


def create_requirement(req: Requirement) -> Requirement:
    with SessionLocal() as session:
        session.execute(
            text(
                """
            INSERT INTO requirements (id, text, req_type, device_type)
            VALUES (:id, :text, :req_type, :device_type)
        """
            ),
            req.model_dump(),
        )
        session.commit()
        return req


def delete_requirement(req_id: int) -> bool:
    with SessionLocal() as session:
        result = session.execute(
            text(
                """
            DELETE FROM requirements WHERE id = :req_id
        """
            ),
            {"req_id": req_id},
        )
        session.commit()
        return result.rowcount > 0


def get_all_testcases() -> List[TestCase]:
    with SessionLocal() as session:
        result = session.execute(
            text(
                """
            SELECT id, requirement_id, description, steps, expected_result
            FROM test_cases
        """
            )
        )
        return [TestCase(**row._asdict()) for row in result]


def get_testcase_by_id(testcase_id: int) -> Optional[TestCase]:
    with SessionLocal() as session:
        result = session.execute(
            text(
                """
            SELECT id, requirement_id, description, steps, expected_result
            FROM test_cases
            WHERE id = :testcase_id
        """
            ),
            {"testcase_id": testcase_id},
        )
        row = result.fetchone()
        return TestCase(**row._asdict()) if row else None


def create_testcase(tc: TestCase) -> TestCase:
    with SessionLocal() as session:
        session.execute(
            text(
                """
            INSERT INTO test_cases
            (id, requirement_id, description, steps, expected_result)
            VALUES (:id, :requirement_id, :description, :steps, :expected_result)
        """
            ),
            tc.model_dump(),
        )
        session.commit()
        return tc


def delete_testcase(testcase_id: int) -> bool:
    with SessionLocal() as session:
        result = session.execute(
            text(
                """
            DELETE FROM test_cases WHERE id = :testcase_id
        """
            ),
            {"testcase_id": testcase_id},
        )
        session.commit()
        return result.rowcount > 0


def get_all_requirement_ids() -> set[int]:
    with SessionLocal() as session:
        result = session.execute(text("SELECT id FROM requirements"))
        return {row.id for row in result}
