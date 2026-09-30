import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Course(Base):
    __tablename__ = "courses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)
    difficulty = Column(String(50), default="Beginner")  # Beginner, Intermediate, Advanced
    language = Column(String(20), default="en")
    duration_minutes = Column(Integer, default=60)
    provider_id = Column(String(36), nullable=True)
    status = Column(String(50), default="Published")  # Draft, Published, Archived
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class CourseLesson(Base):
    __tablename__ = "course_lessons"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content_type = Column(String(50), default="Text")  # Video, Audio, Text, Interactive
    content_url = Column(String(500), nullable=True)
    text_content = Column(Text, nullable=True)
    sequence_number = Column(Integer, default=1)
    duration_minutes = Column(Integer, default=15)

class CourseSkill(Base):
    __tablename__ = "course_skills"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False)
    expected_improvement = Column(Integer, default=1)  # Skill points improvement

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    member_id = Column(String(36), ForeignKey("member_profiles.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    status = Column(String(50), default="Enrolled")  # Enrolled, In Progress, Completed
    progress_percentage = Column(Float, default=0.0)
    enrolled_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
