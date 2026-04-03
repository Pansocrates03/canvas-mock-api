"""
Canvas Mock API – Courses Endpoints
Implements: https://canvas.instructure.com/doc/api/courses.html
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from copy import deepcopy

from core.auth import get_current_user, require_teacher
from data.mock_data import (
    COURSES, ENROLLMENTS, USERS, SECTIONS, ASSIGNMENTS, ASSIGNMENT_GROUPS,
    PAGES, MODULES, ANNOUNCEMENTS, DISCUSSION_TOPICS, next_id
)

router = APIRouter(prefix="/api/v1", tags=["Courses"])


def _enrich_course(course: dict, current_user: dict) -> dict:
    """Add enrollment info if the user is enrolled."""
    c = deepcopy(course)
    user_enrollments = [e for e in ENROLLMENTS.values() if e["course_id"] == c["id"] and e["user_id"] == current_user["id"]]
    if user_enrollments:
        c["enrollments"] = user_enrollments
    return c


# ─── List / Search ─────────────────────────────────────────────────────────────

@router.get("/courses", summary="List active courses for the current user")
async def list_courses(
    enrollment_type: Optional[str] = Query(None, description="Filter by enrollment type: teacher, student, ta, observer, designer"),
    enrollment_state: Optional[str] = Query("active", description="Filter by enrollment state"),
    exclude_blueprint_courses: bool = Query(False),
    include: Optional[List[str]] = Query(None, description="Additional data to include: syllabus_body, term, course_progress, storage_quota_used_mb, total_students, teachers, account_name, concluded"),
    state: Optional[List[str]] = Query(None, description="Course state: unpublished, available, completed, deleted"),
    current_user=Depends(get_current_user),
):
    user_course_ids = {e["course_id"] for e in ENROLLMENTS.values() if e["user_id"] == current_user["id"]}
    result = []
    for cid, course in COURSES.items():
        if cid not in user_course_ids:
            continue
        if enrollment_type:
            enr = next((e for e in ENROLLMENTS.values() if e["course_id"] == cid and e["user_id"] == current_user["id"]), None)
            if not enr or enrollment_type.lower() not in enr["type"].lower():
                continue
        c = _enrich_course(course, current_user)
        if include:
            if "syllabus_body" not in include:
                c.pop("syllabus_body", None)
            if "term" not in include:
                c.pop("term", None)
        result.append(c)
    return result


@router.get("/courses/{course_id}", summary="Get a single course")
async def get_course(
    course_id: int,
    include: Optional[List[str]] = Query(None),
    current_user=Depends(get_current_user),
):
    course = COURSES.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail={"errors": [{"type": "not_found", "message": f"The specified resource does not exist."}]})
    return _enrich_course(course, current_user)


@router.post("/courses", summary="Create a new course")
async def create_course(
    body: dict,
    account_id: int = Query(1),
    current_user=Depends(require_teacher),
):
    course_data = body.get("course", body)
    new_id = next_id("course")
    now = "2024-03-01T00:00:00Z"
    new_course = {
        "id": new_id,
        "name": course_data.get("name", "New Course"),
        "course_code": course_data.get("course_code", f"COURSE{new_id}"),
        "uuid": str(__import__("uuid").uuid4()),
        "sis_course_id": course_data.get("sis_course_id"),
        "integration_id": course_data.get("integration_id"),
        "account_id": account_id,
        "root_account_id": 1,
        "enrollment_term_id": course_data.get("term_id", 1),
        "grading_standard_id": None,
        "start_at": course_data.get("start_at"),
        "end_at": course_data.get("end_at"),
        "created_at": now, "updated_at": now,
        "locale": course_data.get("locale", "en"),
        "enrollments": None, "total_students": 0,
        "calendar": None, "default_view": course_data.get("default_view", "modules"),
        "syllabus_body": course_data.get("syllabus_body"),
        "needs_grading_count": 0, "term": {"id": 1, "name": "Spring 2024"},
        "public_syllabus": course_data.get("public_syllabus", False),
        "public_syllabus_to_auth": course_data.get("public_syllabus_to_auth", False),
        "storage_quota_mb": 500, "is_public": course_data.get("is_public", False),
        "is_public_to_auth_users": False, "hide_final_grades": course_data.get("hide_final_grades", False),
        "license": course_data.get("license", "private"),
        "allow_student_assignment_edits": False, "allow_wiki_comments": False,
        "allow_student_forum_attachments": True, "open_enrollment": course_data.get("open_enrollment", False),
        "self_enrollment": course_data.get("self_enrollment", False),
        "restrict_enrollments_to_course_dates": False,
        "course_format": course_data.get("course_format", "on_campus"),
        "workflow_state": "unpublished", "blueprint": False, "time_zone": "America/Chicago",
        "teacher_id": current_user["id"],
    }
    COURSES[new_id] = new_course
    return new_course


@router.put("/courses/{course_id}", summary="Update a course")
async def update_course(
    course_id: int,
    body: dict,
    current_user=Depends(require_teacher),
):
    course = COURSES.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "The specified resource does not exist."}]})
    updates = body.get("course", body)
    for k, v in updates.items():
        if k in course:
            course[k] = v
    course["updated_at"] = "2024-03-20T00:00:00Z"
    return course


@router.delete("/courses/{course_id}", summary="Delete or conclude a course")
async def delete_course(
    course_id: int,
    event: str = Query(..., description="'delete' or 'conclude'"),
    current_user=Depends(require_teacher),
):
    course = COURSES.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "The specified resource does not exist."}]})
    if event == "delete":
        del COURSES[course_id]
        return {"delete": True}
    elif event == "conclude":
        course["workflow_state"] = "completed"
        return {"conclude": True}
    raise HTTPException(status_code=400, detail={"errors": [{"message": "Invalid event. Must be 'delete' or 'conclude'."}]})


# ─── Enrollments ───────────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/enrollments", summary="List enrollments for a course")
async def list_enrollments(
    course_id: int,
    type: Optional[List[str]] = Query(None),
    state: Optional[List[str]] = Query(None),
    current_user=Depends(get_current_user),
):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    result = [e for e in ENROLLMENTS.values() if e["course_id"] == course_id]
    if type:
        result = [e for e in result if e["type"] in type]
    if state:
        result = [e for e in result if e["enrollment_state"] in state]
    for e in result:
        user = USERS.get(e["user_id"], {})
        e_copy = deepcopy(e)
        e_copy["user"] = {"id": user.get("id"), "name": user.get("name"), "login_id": user.get("login_id"), "avatar_url": user.get("avatar_url")}
        e_copy["course"] = {"id": course_id, "name": COURSES[course_id]["name"]}
    return result


@router.post("/courses/{course_id}/enrollments", summary="Enroll a user in a course")
async def enroll_user(
    course_id: int,
    body: dict,
    current_user=Depends(require_teacher),
):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    enr_data = body.get("enrollment", body)
    user_id = enr_data.get("user_id")
    if not user_id or user_id not in USERS:
        raise HTTPException(status_code=400, detail={"errors": [{"message": "Invalid user_id."}]})
    eid = next_id("enrollment")
    new_enr = {
        "id": eid, "course_id": course_id, "user_id": user_id,
        "type": enr_data.get("type", "StudentEnrollment"),
        "enrollment_state": enr_data.get("enrollment_state", "active"),
        "role": enr_data.get("type", "StudentEnrollment"),
        "role_id": 3, "created_at": "2024-03-20T00:00:00Z", "updated_at": "2024-03-20T00:00:00Z",
        "grades": None, "html_url": f"/courses/{course_id}/users/{user_id}", "last_activity_at": None,
    }
    ENROLLMENTS[eid] = new_enr
    return new_enr


@router.delete("/courses/{course_id}/enrollments/{enrollment_id}", summary="Conclude, deactivate or delete an enrollment")
async def delete_enrollment(
    course_id: int,
    enrollment_id: int,
    task: str = Query(..., description="'conclude', 'delete', 'inactivate', or 'deactivate'"),
    current_user=Depends(require_teacher),
):
    enr = ENROLLMENTS.get(enrollment_id)
    if not enr or enr["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Enrollment not found."}]})
    if task == "delete":
        del ENROLLMENTS[enrollment_id]
        return enr
    enr["enrollment_state"] = "inactive" if task in ("inactivate", "deactivate") else "completed"
    return enr


# ─── Students / Users ──────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/students", summary="List students enrolled in a course")
async def list_students(course_id: int, current_user=Depends(get_current_user)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    student_ids = [e["user_id"] for e in ENROLLMENTS.values() if e["course_id"] == course_id and e["type"] == "StudentEnrollment"]
    return [deepcopy(USERS[uid]) for uid in student_ids if uid in USERS]


@router.get("/courses/{course_id}/users", summary="List users in a course")
async def list_course_users(
    course_id: int,
    enrollment_type: Optional[List[str]] = Query(None),
    include: Optional[List[str]] = Query(None),
    current_user=Depends(get_current_user),
):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    enrollments = [e for e in ENROLLMENTS.values() if e["course_id"] == course_id]
    if enrollment_type:
        enrollments = [e for e in enrollments if any(t.lower() in e["type"].lower() for t in enrollment_type)]
    result = []
    for e in enrollments:
        user = deepcopy(USERS.get(e["user_id"], {}))
        if include and "enrollments" in include:
            user["enrollments"] = [e]
        result.append(user)
    return result


@router.get("/courses/{course_id}/users/{user_id}", summary="Get a single user in a course")
async def get_course_user(course_id: int, user_id: int, current_user=Depends(get_current_user)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    enr = next((e for e in ENROLLMENTS.values() if e["course_id"] == course_id and e["user_id"] == user_id), None)
    if not enr:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "User not enrolled in this course."}]})
    return deepcopy(USERS.get(user_id, {}))


# ─── Sections ──────────────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/sections", summary="List sections of a course")
async def list_sections(course_id: int, current_user=Depends(get_current_user)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    return [s for s in SECTIONS.values() if s["course_id"] == course_id]


# ─── Assignment Groups ─────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/assignment_groups", summary="List assignment groups for a course")
async def list_assignment_groups(course_id: int, current_user=Depends(get_current_user)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    return [ag for ag in ASSIGNMENT_GROUPS.values() if ag["course_id"] == course_id]


# ─── Grading Standards ─────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/grading_standards", summary="Get grading standards for a course")
async def get_grading_standards(course_id: int, current_user=Depends(get_current_user)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    return [{
        "id": 1, "title": "Default Grading Standard",
        "context_type": "Course", "context_id": course_id,
        "grading_scheme": [
            {"name": "A", "value": 0.94}, {"name": "A-", "value": 0.90}, {"name": "B+", "value": 0.87},
            {"name": "B", "value": 0.84}, {"name": "B-", "value": 0.80}, {"name": "C+", "value": 0.77},
            {"name": "C", "value": 0.74}, {"name": "C-", "value": 0.70}, {"name": "D+", "value": 0.67},
            {"name": "D", "value": 0.64}, {"name": "D-", "value": 0.61}, {"name": "F", "value": 0.0},
        ],
    }]


# ─── Tabs ───────────────────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/tabs", summary="List available tabs for a course")
async def list_tabs(course_id: int, current_user=Depends(get_current_user)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    return [
        {"id": "home",        "html_url": f"/courses/{course_id}",              "full_url": f"https://mock.university.edu/courses/{course_id}",              "position": 1, "type": "internal", "label": "Home",          "hidden": False},
        {"id": "modules",     "html_url": f"/courses/{course_id}/modules",      "full_url": f"https://mock.university.edu/courses/{course_id}/modules",      "position": 2, "type": "internal", "label": "Modules",       "hidden": False},
        {"id": "assignments", "html_url": f"/courses/{course_id}/assignments",  "full_url": f"https://mock.university.edu/courses/{course_id}/assignments",  "position": 3, "type": "internal", "label": "Assignments",   "hidden": False},
        {"id": "quizzes",     "html_url": f"/courses/{course_id}/quizzes",      "full_url": f"https://mock.university.edu/courses/{course_id}/quizzes",      "position": 4, "type": "internal", "label": "Quizzes",       "hidden": False},
        {"id": "pages",       "html_url": f"/courses/{course_id}/pages",        "full_url": f"https://mock.university.edu/courses/{course_id}/pages",        "position": 5, "type": "internal", "label": "Pages",         "hidden": False},
        {"id": "grades",      "html_url": f"/courses/{course_id}/grades",       "full_url": f"https://mock.university.edu/courses/{course_id}/grades",       "position": 6, "type": "internal", "label": "Grades",        "hidden": False},
        {"id": "people",      "html_url": f"/courses/{course_id}/users",        "full_url": f"https://mock.university.edu/courses/{course_id}/users",        "position": 7, "type": "internal", "label": "People",        "hidden": False},
        {"id": "discussions", "html_url": f"/courses/{course_id}/discussion_topics", "full_url": f"https://mock.university.edu/courses/{course_id}/discussion_topics", "position": 8, "type": "internal", "label": "Discussions", "hidden": False},
        {"id": "announcements","html_url": f"/courses/{course_id}/announcements","full_url": f"https://mock.university.edu/courses/{course_id}/announcements","position": 9, "type": "internal", "label": "Announcements", "hidden": False},
    ]
