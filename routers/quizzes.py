"""
Canvas Mock API – Quizzes, Quiz Questions, Quiz Submissions
Implements:
  https://canvas.instructure.com/doc/api/quizzes.html
  https://canvas.instructure.com/doc/api/quiz_questions.html
  https://canvas.instructure.com/doc/api/quiz_submissions.html
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from copy import deepcopy

from core.auth import get_current_user, require_teacher
from data.mock_data import (
    COURSES, QUIZZES, QUIZ_QUESTIONS, QUIZ_SUBMISSIONS, ENROLLMENTS, USERS, next_id
)

router = APIRouter(prefix="/api/v1", tags=["Quizzes"])


def _check_course(course_id: int):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})


# ─── Quizzes ───────────────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/quizzes", summary="List quizzes for a course")
async def list_quizzes(
    course_id: int,
    search_term: Optional[str] = Query(None),
    current_user=Depends(get_current_user),
):
    _check_course(course_id)
    result = [q for q in QUIZZES.values() if q["course_id"] == course_id]
    if search_term:
        result = [q for q in result if search_term.lower() in q["title"].lower()]
    return result


@router.get("/courses/{course_id}/quizzes/{quiz_id}", summary="Get a single quiz")
async def get_quiz(course_id: int, quiz_id: int, current_user=Depends(get_current_user)):
    _check_course(course_id)
    quiz = QUIZZES.get(quiz_id)
    if not quiz or quiz["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Quiz not found."}]})
    return deepcopy(quiz)


@router.post("/courses/{course_id}/quizzes", summary="Create a quiz")
async def create_quiz(course_id: int, body: dict, current_user=Depends(require_teacher)):
    _check_course(course_id)
    qdata = body.get("quiz", body)
    new_id = next_id("quiz")
    now = "2024-03-20T00:00:00Z"
    new_quiz = {
        "id": new_id, "course_id": course_id,
        "title": qdata.get("title", "New Quiz"),
        "html_url": f"/courses/{course_id}/quizzes/{new_id}",
        "mobile_url": f"/courses/{course_id}/quizzes/{new_id}?persist_headless=1",
        "description": qdata.get("description", ""),
        "quiz_type": qdata.get("quiz_type", "assignment"),
        "time_limit": qdata.get("time_limit"),
        "timer_autosubmit_disabled": qdata.get("timer_autosubmit_disabled", False),
        "shuffle_answers": qdata.get("shuffle_answers", False),
        "show_correct_answers": qdata.get("show_correct_answers", True),
        "show_correct_answers_last_attempt": qdata.get("show_correct_answers_last_attempt", False),
        "show_correct_answers_at": qdata.get("show_correct_answers_at"),
        "hide_correct_answers_at": qdata.get("hide_correct_answers_at"),
        "hide_results": qdata.get("hide_results"),
        "one_time_results": qdata.get("one_time_results", False),
        "scoring_policy": qdata.get("scoring_policy", "keep_highest"),
        "allowed_attempts": qdata.get("allowed_attempts", 1),
        "one_question_at_a_time": qdata.get("one_question_at_a_time", False),
        "question_count": 0, "points_possible": 0.0,
        "cant_go_back": qdata.get("cant_go_back", False),
        "access_code": qdata.get("access_code"),
        "ip_filter": qdata.get("ip_filter"),
        "due_at": qdata.get("due_at"), "lock_at": qdata.get("lock_at"),
        "unlock_at": qdata.get("unlock_at"),
        "published": qdata.get("published", False),
        "unpublishable": True, "locked_for_user": False,
        "lock_info": None, "lock_explanation": None,
        "speedgrader_url": None, "quiz_extensions_url": f"/courses/{course_id}/quizzes/{new_id}/extensions",
        "permissions": {"read": True, "submit": True, "create": True, "manage": True, "read_statistics": True, "review_grades": True, "update": True},
        "all_dates": [], "version_number": 1, "question_types": [],
        "has_access_code": bool(qdata.get("access_code")), "assignment_id": None,
        "created_at": now, "updated_at": now,
    }
    QUIZZES[new_id] = new_quiz
    QUIZ_QUESTIONS[new_id] = []
    return new_quiz


@router.put("/courses/{course_id}/quizzes/{quiz_id}", summary="Update a quiz")
async def update_quiz(course_id: int, quiz_id: int, body: dict, current_user=Depends(require_teacher)):
    _check_course(course_id)
    quiz = QUIZZES.get(quiz_id)
    if not quiz or quiz["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Quiz not found."}]})
    updates = body.get("quiz", body)
    for k, v in updates.items():
        if k in quiz:
            quiz[k] = v
    quiz["updated_at"] = "2024-03-20T00:00:00Z"
    return quiz


@router.delete("/courses/{course_id}/quizzes/{quiz_id}", summary="Delete a quiz")
async def delete_quiz(course_id: int, quiz_id: int, current_user=Depends(require_teacher)):
    _check_course(course_id)
    quiz = QUIZZES.get(quiz_id)
    if not quiz or quiz["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Quiz not found."}]})
    del QUIZZES[quiz_id]
    return deepcopy(quiz)


@router.post("/courses/{course_id}/quizzes/{quiz_id}/reorder", summary="Reorder quiz items")
async def reorder_quiz_items(course_id: int, quiz_id: int, body: dict, current_user=Depends(require_teacher)):
    _check_course(course_id)
    if quiz_id not in QUIZZES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Quiz not found."}]})
    return {"reorder": True}


# ─── Quiz Questions ────────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/quizzes/{quiz_id}/questions", summary="List quiz questions")
async def list_questions(
    course_id: int,
    quiz_id: int,
    quiz_submission_id: Optional[int] = Query(None),
    quiz_submission_attempt: Optional[int] = Query(None),
    current_user=Depends(get_current_user),
):
    _check_course(course_id)
    if quiz_id not in QUIZZES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Quiz not found."}]})
    return deepcopy(QUIZ_QUESTIONS.get(quiz_id, []))


@router.get("/courses/{course_id}/quizzes/{quiz_id}/questions/{question_id}", summary="Get a single quiz question")
async def get_question(course_id: int, quiz_id: int, question_id: int, current_user=Depends(get_current_user)):
    _check_course(course_id)
    questions = QUIZ_QUESTIONS.get(quiz_id, [])
    q = next((q for q in questions if q["id"] == question_id), None)
    if not q:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Question not found."}]})
    return deepcopy(q)


@router.post("/courses/{course_id}/quizzes/{quiz_id}/questions", summary="Create a quiz question")
async def create_question(course_id: int, quiz_id: int, body: dict, current_user=Depends(require_teacher)):
    _check_course(course_id)
    if quiz_id not in QUIZZES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Quiz not found."}]})
    qdata = body.get("question", body)
    existing = QUIZ_QUESTIONS.get(quiz_id, [])
    new_id = max((q["id"] for q in existing), default=0) + 1
    pos = max((q["position"] for q in existing), default=0) + 1
    new_q = {
        "id": new_id, "quiz_id": quiz_id,
        "position": qdata.get("position", pos),
        "question_name": qdata.get("question_name", f"Question {new_id}"),
        "question_type": qdata.get("question_type", "multiple_choice_question"),
        "question_text": qdata.get("question_text", ""),
        "points_possible": qdata.get("points_possible", 1.0),
        "correct_comments": qdata.get("correct_comments", ""),
        "incorrect_comments": qdata.get("incorrect_comments", ""),
        "neutral_comments": qdata.get("neutral_comments", ""),
        "answers": qdata.get("answers", []),
    }
    existing.append(new_q)
    QUIZ_QUESTIONS[quiz_id] = existing
    # Update question count and points on quiz
    quiz = QUIZZES[quiz_id]
    quiz["question_count"] = len(existing)
    quiz["points_possible"] = sum(q.get("points_possible", 0) for q in existing)
    return new_q


@router.put("/courses/{course_id}/quizzes/{quiz_id}/questions/{question_id}", summary="Update a quiz question")
async def update_question(course_id: int, quiz_id: int, question_id: int, body: dict, current_user=Depends(require_teacher)):
    _check_course(course_id)
    questions = QUIZ_QUESTIONS.get(quiz_id, [])
    q = next((q for q in questions if q["id"] == question_id), None)
    if not q:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Question not found."}]})
    updates = body.get("question", body)
    q.update(updates)
    return q


@router.delete("/courses/{course_id}/quizzes/{quiz_id}/questions/{question_id}", summary="Delete a quiz question")
async def delete_question(course_id: int, quiz_id: int, question_id: int, current_user=Depends(require_teacher)):
    _check_course(course_id)
    questions = QUIZ_QUESTIONS.get(quiz_id, [])
    q = next((q for q in questions if q["id"] == question_id), None)
    if not q:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Question not found."}]})
    QUIZ_QUESTIONS[quiz_id] = [x for x in questions if x["id"] != question_id]
    quiz = QUIZZES.get(quiz_id)
    if quiz:
        quiz["question_count"] = len(QUIZ_QUESTIONS[quiz_id])
    return {}


# ─── Quiz Submissions ──────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/quizzes/{quiz_id}/submissions", summary="List quiz submissions")
async def list_quiz_submissions(
    course_id: int,
    quiz_id: int,
    include: Optional[List[str]] = Query(None),
    current_user=Depends(get_current_user),
):
    _check_course(course_id)
    if quiz_id not in QUIZZES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Quiz not found."}]})
    subs = [s for s in QUIZ_SUBMISSIONS.values() if s["quiz_id"] == quiz_id]
    result = {"quiz_submissions": subs}
    if include and "quiz" in include:
        result["quizzes"] = [deepcopy(QUIZZES[quiz_id])]
    if include and "submission" in include:
        result["submissions"] = subs
    if include and "user" in include:
        uids = {s["user_id"] for s in subs}
        result["users"] = [deepcopy(USERS[uid]) for uid in uids if uid in USERS]
    return result


@router.get("/courses/{course_id}/quizzes/{quiz_id}/submissions/{submission_id}", summary="Get a single quiz submission")
async def get_quiz_submission(course_id: int, quiz_id: int, submission_id: int, current_user=Depends(get_current_user)):
    _check_course(course_id)
    sub = QUIZ_SUBMISSIONS.get(submission_id)
    if not sub or sub["quiz_id"] != quiz_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Submission not found."}]})
    return {"quiz_submissions": [deepcopy(sub)]}


@router.post("/courses/{course_id}/quizzes/{quiz_id}/submissions", summary="Start a quiz taking session (create submission)")
async def create_quiz_submission(
    course_id: int,
    quiz_id: int,
    body: Optional[dict] = None,
    current_user=Depends(get_current_user),
):
    _check_course(course_id)
    quiz = QUIZZES.get(quiz_id)
    if not quiz or quiz["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Quiz not found."}]})
    new_id = max(QUIZ_SUBMISSIONS.keys(), default=0) + 1
    now = "2024-03-20T10:00:00Z"
    end_at = quiz.get("time_limit") and f"2024-03-20T{10 + quiz['time_limit'] // 60}:00:00Z"
    sub = {
        "id": new_id, "quiz_id": quiz_id, "user_id": current_user["id"],
        "course_id": course_id, "submission_id": 200 + new_id,
        "started_at": now, "finished_at": None,
        "end_at": end_at or quiz.get("due_at"),
        "attempt": 1, "extra_attempts": None, "extra_time": None,
        "time_spent": 0, "score": None, "score_before_regrade": None,
        "kept_score": None, "fudge_points": None,
        "workflow_state": "untaken",
        "quiz_points_possible": quiz.get("points_possible", 0),
        "quiz_version": quiz.get("version_number", 1),
        "html_url": f"/courses/{course_id}/quizzes/{quiz_id}/submissions/{new_id}",
    }
    QUIZ_SUBMISSIONS[new_id] = sub
    return {"quiz_submissions": [sub], "quizzes": [deepcopy(quiz)]}


@router.put("/courses/{course_id}/quizzes/{quiz_id}/submissions/{submission_id}", summary="Complete a quiz submission")
async def complete_quiz_submission(
    course_id: int, quiz_id: int, submission_id: int,
    body: dict, current_user=Depends(get_current_user),
):
    _check_course(course_id)
    sub = QUIZ_SUBMISSIONS.get(submission_id)
    if not sub or sub["quiz_id"] != quiz_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Submission not found."}]})
    sub_data = body.get("quiz_submission", body)
    sub["attempt"] = sub_data.get("attempt", sub["attempt"])
    sub["validation_token"] = sub_data.get("validation_token")
    sub["workflow_state"] = "complete"
    sub["finished_at"] = "2024-03-20T10:28:00Z"
    sub["time_spent"] = 1680
    return {"quiz_submissions": [deepcopy(sub)]}


# ─── Quiz IP Filters ───────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/quizzes/{quiz_id}/ip_filters", summary="List quiz IP filters")
async def list_ip_filters(course_id: int, quiz_id: int, current_user=Depends(get_current_user)):
    _check_course(course_id)
    quiz = QUIZZES.get(quiz_id)
    if not quiz or quiz["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Quiz not found."}]})
    return {"quiz_ip_filters": [] if not quiz.get("ip_filter") else [{"name": "Campus Network", "account": "University of Mock", "filter": quiz["ip_filter"]}]}


# ─── Quiz Extensions ───────────────────────────────────────────────────────────

@router.post("/courses/{course_id}/quizzes/{quiz_id}/extensions", summary="Create quiz extensions for users")
async def create_quiz_extensions(
    course_id: int, quiz_id: int, body: dict, current_user=Depends(require_teacher),
):
    _check_course(course_id)
    if quiz_id not in QUIZZES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Quiz not found."}]})
    extensions = body.get("quiz_extensions", [])
    result = []
    for ext in extensions:
        result.append({
            "user_id": ext.get("user_id"),
            "quiz_id": quiz_id,
            "extra_attempts": ext.get("extra_attempts", 0),
            "extra_time": ext.get("extra_time", 0),
            "manually_unlocked": ext.get("manually_unlocked", False),
            "end_at": ext.get("end_at"),
        })
    return {"quiz_extensions": result}
