from fastapi import APIRouter, Depends
from core.dependencies import verify_token
from core.mock_db import MOCK_QUIZZES, MOCK_QUIZ_STATS

# Nota: Canvas anida los quizzes dentro de courses
router = APIRouter(
    prefix="/api/v1/courses/{course_id}/quizzes",
    tags=["Quizzes", "Quiz Statistics"],
    dependencies=[Depends(verify_token)]
)

@router.get("/")
async def list_quizzes_in_course(course_id: int):
    return [q for q in MOCK_QUIZZES if q["course_id"] == course_id]

@router.get("/{quiz_id}/statistics")
async def get_quiz_statistics(course_id: int, quiz_id: int):
    stats = [s for s in MOCK_QUIZ_STATS if s["quiz_id"] == quiz_id]
    if not stats:
        return {"quiz_statistics": []}
    return {"quiz_statistics": stats}