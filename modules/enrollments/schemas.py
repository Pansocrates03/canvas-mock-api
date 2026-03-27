from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class GradeModel(BaseModel):
    html_url: str
    current_score: Optional[float] = None
    current_grade: Optional[str] = None
    final_score: Optional[float] = None
    final_grade: Optional[str] = None

class EnrollmentModel(BaseModel):
    id: int
    course_id: int
    course_section_id: int
    enrollment_state: str = Field(..., description="Estado: 'active', 'invited', 'inactive', 'deleted'")
    limit_privileges_to_course_section: bool = False
    root_account_id: int
    type: str = Field(..., description="Rol: 'StudentEnrollment', 'TeacherEnrollment', etc.")
    user_id: int
    role: str
    role_id: int
    created_at: datetime
    updated_at: datetime
    total_activity_time: int = 0
    html_url: str
    grades: Optional[GradeModel] = None
    user: Optional[Dict[str, Any]] = None