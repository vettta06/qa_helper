from sqlalchemy import create_engine, Column, Integer, String, ARRAY, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://qa_user:qa_pass@localhost/qa_helper")

Base = declarative_base()


class Requirement(Base):
    __tablename__ = "requirements"
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    req_type = Column(String, nullable=False)
    device_type = Column(String, nullable=False)


class TestCase(Base):
    __tablename__ = "test_cases"
    id = Column(Integer, primary_key=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    description = Column(String, nullable=False)
    steps = Column(ARRAY(String), nullable=False)
    expected_result = Column(String, nullable=False)


class BugReport(Base):
    __tablename__ = "bug_reports"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    steps_to_reproduce = Column(ARRAY(String), nullable=False)
    actual_result = Column(String, nullable=False)
    expected_result = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    test_case_id = Column(Integer, nullable=True)


Base.metadata.create_all(engine)
print("Таблицы созданы!")
