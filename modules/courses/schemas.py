from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class CourseModel(BaseModel):
    id: int
    sis_course_id: Optional[str] = None
    uuid: str
    integration_id: Optional[str] = None
    sis_import_id: Optional[int] = None
    name: str
    course_code: str
    original_name: Optional[str] = None
    workflow_state: str = Field(..., description="Estado actual del curso")
    account_id: int
    root_account_id: int
    enrollment_term_id: int
    grading_periods: Optional[List[Dict[str, Any]]] = None
    grading_standard_id: Optional[int] = None
    grade_passback_setting: Optional[str] = None
    created_at: datetime
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    locale: Optional[str] = None
    enrollments: Optional[List[Dict[str, Any]]] = None
    total_students: Optional[int] = None
    calendar: Optional[Dict[str, Any]] = None
    default_view: str
    syllabus_body: Optional[str] = None
    needs_grading_count: Optional[int] = None
    term: Optional[Dict[str, Any]] = None
    course_progress: Optional[Dict[str, Any]] = None
    apply_assignment_group_weights: bool
    permissions: Optional[Dict[str, bool]] = None
    is_public: bool
    is_public_to_auth_users: bool
    public_syllabus: bool
    public_syllabus_to_auth: bool
    public_description: Optional[str] = None
    storage_quota_mb: int
    storage_quota_used_mb: float
    hide_final_grades: bool
    license: str
    allow_student_assignment_edits: bool
    allow_wiki_comments: bool
    allow_student_forum_attachments: bool
    open_enrollment: Optional[bool] = None
    self_enrollment: Optional[bool] = None
    restrict_enrollments_to_course_dates: bool
    course_format: Optional[str] = None
    access_restricted_by_date: Optional[bool] = None
    time_zone: str
    blueprint: Optional[bool] = None
    blueprint_restrictions: Optional[Dict[str, bool]] = None
    blueprint_restrictions_by_object_type: Optional[Dict[str, Dict[str, bool]]] = None
    template: Optional[bool] = None