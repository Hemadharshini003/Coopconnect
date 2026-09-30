import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    lesson_id = Column(String(36), ForeignKey("course_lessons.id"), nullable=True)
    title = Column(String(255), nullable=False)
    generated_by_ai = Column(Boolean, default=True)
    status = Column(String(50), default="Approved")  # Pending Trainer Approval, Approved, Rejected

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    quiz_id = Column(String(36), ForeignKey("quizzes.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="MCQ")  # MCQ, Boolean, ShortAnswer
    options_json = Column(Text, nullable=True)  # JSON string of choices
    correct_answer = Column(String(255), nullable=False)
    explanation = Column(Text, nullable=True)
    marks = Column(Integer, default=10)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    quiz_id = Column(String(36), ForeignKey("quizzes.id"), nullable=False)
    member_id = Column(String(36), ForeignKey("member_profiles.id"), nullable=False)
    score = Column(Float, default=0.0)
    passed = Column(Boolean, default=False)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    member_id = Column(String(36), ForeignKey("member_profiles.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    certificate_number = Column(String(100), unique=True, nullable=False)
    issued_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    certificate_url = Column(String(500), nullable=True)
