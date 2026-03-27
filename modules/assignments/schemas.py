from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class AssignmentModel(BaseModel):
    id: int
    course_id: int
    name: str
    description: Optional[str] = None
    due_at: Optional[datetime] = None
    unlock_at: Optional[datetime] = None
    lock_at: Optional[datetime] = None
    points_possible: Optional[float] = None
    submission_types: List[str] = Field(
        default=["none"], 
        description="Ej. 'online_quiz', 'none', 'on_paper', 'online_upload'"
    )
    allowed_extensions: Optional[List[str]] = None
    grading_type: str = Field(
        default="points",
        description="'pass_fail', 'percent', 'letter_grade', 'gpa_scale', 'points'"
    )
    published: bool = False
    html_url: str
    needs_grading_count: Optional[int] = 0
    has_submitted_submissions: Optional[bool] = False
    omit_from_final_grade: Optional[bool] = False