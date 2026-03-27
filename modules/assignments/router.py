from fastapi import APIRouter, Depends, HTTPException
from typing import List

from core.dependencies import verify_token
from core.mock_db import MOCK_ASSIGNMENTS
from modules.assignments.schemas import AssignmentModel

router = APIRouter(
    prefix="/api/v1/courses/{course_id}/assignments",
    tags=["Assignments"],
    dependencies=[Depends(verify_token)]
)

@router.get("/", response_model=List[AssignmentModel])
async def list_assignments(course_id: int):
    """Obtiene todas las tareas de un curso."""
    return [a for a in MOCK_ASSIGNMENTS if a["course_id"] == course_id]

@router.get("/{assignment_id}", response_model=AssignmentModel)
async def get_assignment(course_id: int, assignment_id: int):
    """Obtiene una tarea específica."""
    assignment = next(
        (a for a in MOCK_ASSIGNMENTS if a["id"] == assignment_id and a["course_id"] == course_id), 
        None
    )
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment