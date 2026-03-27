from fastapi import APIRouter, Depends
from typing import List

from core.dependencies import verify_token
from core.mock_db import MOCK_ENROLLMENTS
from modules.enrollments.schemas import EnrollmentModel

router = APIRouter(
    tags=["Enrollments"],
    dependencies=[Depends(verify_token)]
)

@router.get("/api/v1/courses/{course_id}/enrollments", response_model=List[EnrollmentModel])
async def list_enrollments_by_course(course_id: int):
    return [e for e in MOCK_ENROLLMENTS if e["course_id"] == course_id]

@router.get("/api/v1/users/{user_id}/enrollments", response_model=List[EnrollmentModel])
async def list_enrollments_by_user(user_id: int):
    return [e for e in MOCK_ENROLLMENTS if e["user_id"] == user_id]