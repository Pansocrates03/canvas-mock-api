from fastapi import APIRouter, Depends, HTTPException
from typing import List

from core.dependencies import verify_token
from core.mock_db import MOCK_COURSES
from modules.courses.schemas import CourseModel

router = APIRouter(
    prefix="/api/v1/courses",
    tags=["Courses"],
    dependencies=[Depends(verify_token)]
)

@router.get("/", response_model=List[CourseModel])
async def list_courses():
    """
    Lista todos los cursos simulados.
    """
    return MOCK_COURSES

@router.get("/{course_id}", response_model=CourseModel)
async def get_course(course_id: int):
    """
    Obtiene los detalles de un curso específico por su ID.
    """
    course = next((c for c in MOCK_COURSES if c["id"] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course