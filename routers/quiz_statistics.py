"""
Canvas Mock API – Quiz Statistics
Implements: https://canvas.instructure.com/doc/api/quiz_statistics.html
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from copy import deepcopy

from core.auth import get_current_user
from data.mock_data import COURSES, QUIZZES, QUIZ_STATISTICS, QUIZ_SUBMISSIONS

router = APIRouter(prefix="/api/v1", tags=["Quiz Statistics"])


@router.get(
    "/courses/{course_id}/quizzes/{quiz_id}/statistics",
    summary="List quiz statistics",
    description="Returns aggregate statistics for a quiz, including submission stats and per-question statistics.",
)
async def list_quiz_statistics(
    course_id: int,
    quiz_id: int,
    all_versions: bool = Query(False, description="Include statistics across all quiz versions"),
    current_user=Depends(get_current_user),
):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    quiz = QUIZZES.get(quiz_id)
    if not quiz or quiz["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Quiz not found."}]})

    # Try stored statistics first, otherwise build a minimal on-the-fly response
    stats = deepcopy(QUIZ_STATISTICS.get(quiz_id))
    if not stats:
        subs = [s for s in QUIZ_SUBMISSIONS.values() if s["quiz_id"] == quiz_id]
        scores = [s["score"] for s in subs if s.get("score") is not None]
        stats = {
            "id": quiz_id * 10,
            "quiz_id": quiz_id,
            "course_id": course_id,
            "anonymous_survey": False,
            "speed_grader_url": f"/courses/{course_id}/gradebook/speed_grader?assignment_id={quiz.get('assignment_id')}",
            "quiz_submissions_zip_url": f"/courses/{course_id}/quizzes/{quiz_id}/submissions?zip=1",
            "points_possible": quiz.get("points_possible", 0),
            "multiple_attempts_exist": quiz.get("allowed_attempts", 1) > 1,
            "generated_at": "2024-03-20T00:00:00Z",
            "includes_all_versions": all_versions,
            "submission_statistics": {
                "score_average": round(sum(scores) / len(scores), 2) if scores else 0,
                "score_high": max(scores) if scores else 0,
                "score_low": min(scores) if scores else 0,
                "score_stdev": 0,
                "correct_count_average": 0,
                "incorrect_count_average": 0,
                "duration_average": round(
                    sum(s.get("time_spent", 0) for s in subs) / len(subs), 2
                ) if subs else 0,
                "unique_count": len({s["user_id"] for s in subs}),
            },
            "question_statistics": [],
        }

    stats["includes_all_versions"] = all_versions
    return {"quiz_statistics": [stats]}
