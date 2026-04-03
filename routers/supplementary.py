"""
Canvas Mock API – Supplementary Routers
Assignments, Submissions, Users, Modules, Announcements, Discussions
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from copy import deepcopy

from core.auth import get_current_user, require_teacher
from data.mock_data import (
    COURSES, ASSIGNMENTS, SUBMISSIONS, USERS, MODULES, MODULE_ITEMS,
    ANNOUNCEMENTS, DISCUSSION_TOPICS, ENROLLMENTS, next_id
)

# ═══════════════════════════════════════════════════════════════════════════════
# ASSIGNMENTS
# ═══════════════════════════════════════════════════════════════════════════════
assignments_router = APIRouter(prefix="/api/v1", tags=["Assignments"])


@assignments_router.get("/courses/{course_id}/assignments", summary="List assignments for a course")
async def list_assignments(
    course_id: int,
    include: Optional[List[str]] = Query(None),
    search_term: Optional[str] = Query(None),
    assignment_ids: Optional[List[int]] = Query(None),
    order_by: Optional[str] = Query("position"),
    current_user=Depends(get_current_user),
):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    result = [deepcopy(a) for a in ASSIGNMENTS.values() if a["course_id"] == course_id]
    if search_term:
        result = [a for a in result if search_term.lower() in a["name"].lower()]
    if assignment_ids:
        result = [a for a in result if a["id"] in assignment_ids]
    result.sort(key=lambda x: x.get("position", 0))
    return result


@assignments_router.get("/courses/{course_id}/assignments/{assignment_id}", summary="Get an assignment")
async def get_assignment(course_id: int, assignment_id: int, current_user=Depends(get_current_user)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    a = ASSIGNMENTS.get(assignment_id)
    if not a or a["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Assignment not found."}]})
    return deepcopy(a)


@assignments_router.post("/courses/{course_id}/assignments", summary="Create an assignment")
async def create_assignment(course_id: int, body: dict, current_user=Depends(require_teacher)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    adata = body.get("assignment", body)
    new_id = next_id("assignment")
    now = "2024-03-20T00:00:00Z"
    pos = max((a["position"] for a in ASSIGNMENTS.values() if a["course_id"] == course_id), default=0) + 1
    new_a = {
        "id": new_id, "course_id": course_id,
        "name": adata.get("name", "New Assignment"),
        "description": adata.get("description", ""),
        "due_at": adata.get("due_at"), "lock_at": adata.get("lock_at"), "unlock_at": adata.get("unlock_at"),
        "created_at": now, "updated_at": now,
        "points_possible": adata.get("points_possible", 0.0),
        "grading_type": adata.get("grading_type", "points"),
        "submission_types": adata.get("submission_types", ["none"]),
        "has_submitted_submissions": False, "published": adata.get("published", True),
        "only_visible_to_overrides": False,
        "assignment_group_id": adata.get("assignment_group_id"),
        "position": pos, "peer_reviews": adata.get("peer_reviews", False),
        "automatic_peer_reviews": False, "grade_group_students_individually": False,
        "anonymous_submissions": adata.get("anonymous_submissions", False),
        "omit_from_final_grade": adata.get("omit_from_final_grade", False),
        "moderated_grading": adata.get("moderated_grading", False),
        "rubric_id": adata.get("rubric_id"),
        "html_url": f"/courses/{course_id}/assignments/{new_id}",
        "needs_grading_count": 0,
    }
    ASSIGNMENTS[new_id] = new_a
    return deepcopy(new_a)


@assignments_router.put("/courses/{course_id}/assignments/{assignment_id}", summary="Update an assignment")
async def update_assignment(course_id: int, assignment_id: int, body: dict, current_user=Depends(require_teacher)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    a = ASSIGNMENTS.get(assignment_id)
    if not a or a["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Assignment not found."}]})
    updates = body.get("assignment", body)
    a.update(updates)
    a["updated_at"] = "2024-03-20T00:00:00Z"
    return deepcopy(a)


@assignments_router.delete("/courses/{course_id}/assignments/{assignment_id}", summary="Delete an assignment")
async def delete_assignment(course_id: int, assignment_id: int, current_user=Depends(require_teacher)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    a = ASSIGNMENTS.get(assignment_id)
    if not a or a["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Assignment not found."}]})
    del ASSIGNMENTS[assignment_id]
    return deepcopy(a)


# ═══════════════════════════════════════════════════════════════════════════════
# SUBMISSIONS
# ═══════════════════════════════════════════════════════════════════════════════
submissions_router = APIRouter(prefix="/api/v1", tags=["Submissions"])


@submissions_router.get("/courses/{course_id}/assignments/{assignment_id}/submissions", summary="List assignment submissions")
async def list_submissions(
    course_id: int,
    assignment_id: int,
    include: Optional[List[str]] = Query(None),
    workflow_state: Optional[str] = Query(None),
    current_user=Depends(get_current_user),
):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    a = ASSIGNMENTS.get(assignment_id)
    if not a or a["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Assignment not found."}]})
    result = [deepcopy(s) for k, s in SUBMISSIONS.items() if k[0] == assignment_id]
    if workflow_state:
        result = [s for s in result if s.get("workflow_state") == workflow_state]
    return result


@submissions_router.get("/courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}", summary="Get a submission")
async def get_submission(course_id: int, assignment_id: int, user_id: int, current_user=Depends(get_current_user)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    sub = SUBMISSIONS.get((assignment_id, user_id))
    if not sub:
        # Return empty submission placeholder
        return {"assignment_id": assignment_id, "user_id": user_id, "workflow_state": "unsubmitted", "score": None, "grade": None}
    return deepcopy(sub)


@submissions_router.post("/courses/{course_id}/assignments/{assignment_id}/submissions", summary="Submit an assignment")
async def submit_assignment(course_id: int, assignment_id: int, body: dict, current_user=Depends(get_current_user)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    a = ASSIGNMENTS.get(assignment_id)
    if not a or a["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Assignment not found."}]})
    sdata = body.get("submission", body)
    now = "2024-03-20T12:00:00Z"
    sub = {
        "id": max((s["id"] for s in SUBMISSIONS.values()), default=200) + 1,
        "assignment_id": assignment_id,
        "user_id": current_user["id"],
        "course_id": course_id,
        "submitted_at": now,
        "graded_at": None, "grader_id": None,
        "score": None, "grade": None,
        "workflow_state": "submitted",
        "submission_type": sdata.get("submission_type", "online_text_entry"),
        "body": sdata.get("body"),
        "url": sdata.get("url"),
        "late": False, "missing": False,
        "attempt": sdata.get("attempt", 1),
        "late_policy_status": None, "points_deducted": None,
        "grade_matches_current_submission": True,
        "attachments": [], "comments": [],
    }
    SUBMISSIONS[(assignment_id, current_user["id"])] = sub
    return deepcopy(sub)


@submissions_router.put("/courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}", summary="Grade a submission")
async def grade_submission(course_id: int, assignment_id: int, user_id: int, body: dict, current_user=Depends(require_teacher)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    sub = SUBMISSIONS.get((assignment_id, user_id))
    if not sub:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Submission not found."}]})
    sdata = body.get("submission", body)
    if "posted_grade" in sdata:
        sub["grade"] = sdata["posted_grade"]
        try:
            sub["score"] = float(sdata["posted_grade"])
        except (ValueError, TypeError):
            sub["score"] = None
    if "excuse" in sdata:
        sub["excused"] = sdata["excuse"]
    sub["graded_at"] = "2024-03-20T12:00:00Z"
    sub["grader_id"] = current_user["id"]
    sub["workflow_state"] = "graded"
    if "comment" in sdata:
        sub.setdefault("comments", []).append({
            "id": len(sub.get("comments", [])) + 1,
            "comment": sdata["comment"]["text_comment"],
            "author": {"id": current_user["id"], "display_name": current_user["name"]},
            "created_at": "2024-03-20T12:00:00Z",
        })
    return deepcopy(sub)


# ═══════════════════════════════════════════════════════════════════════════════
# USERS
# ═══════════════════════════════════════════════════════════════════════════════
users_router = APIRouter(prefix="/api/v1", tags=["Users"])


@users_router.get("/users/self", summary="Get current user's profile")
async def get_self(current_user=Depends(get_current_user)):
    return deepcopy(current_user)


@users_router.get("/users/{user_id}", summary="Get a user's profile")
async def get_user(user_id: int, current_user=Depends(get_current_user)):
    user = USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "User not found."}]})
    return deepcopy(user)


@users_router.get("/users/self/enrollments", summary="List current user's enrollments")
async def get_self_enrollments(
    state: Optional[List[str]] = Query(None),
    type: Optional[List[str]] = Query(None),
    current_user=Depends(get_current_user),
):
    result = [deepcopy(e) for e in ENROLLMENTS.values() if e["user_id"] == current_user["id"]]
    if state:
        result = [e for e in result if e["enrollment_state"] in state]
    if type:
        result = [e for e in result if e["type"] in type]
    return result


@users_router.get("/users/self/courses", summary="List courses for current user (alias)")
async def get_self_courses(current_user=Depends(get_current_user)):
    user_course_ids = {e["course_id"] for e in ENROLLMENTS.values() if e["user_id"] == current_user["id"]}
    return [deepcopy(COURSES[cid]) for cid in user_course_ids if cid in COURSES]


@users_router.get("/accounts/1/users", summary="List users in an account")
async def list_account_users(
    search_term: Optional[str] = Query(None),
    current_user=Depends(require_teacher),
):
    result = list(USERS.values())
    if search_term:
        result = [u for u in result if search_term.lower() in u["name"].lower() or search_term.lower() in u.get("email", "").lower()]
    return [deepcopy(u) for u in result]


# ═══════════════════════════════════════════════════════════════════════════════
# MODULES
# ═══════════════════════════════════════════════════════════════════════════════
modules_router = APIRouter(prefix="/api/v1", tags=["Modules"])


@modules_router.get("/courses/{course_id}/modules", summary="List modules for a course")
async def list_modules(
    course_id: int,
    include: Optional[List[str]] = Query(None),
    search_term: Optional[str] = Query(None),
    student_id: Optional[int] = Query(None),
    current_user=Depends(get_current_user),
):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    result = [deepcopy(m) for m in MODULES.values() if m["course_id"] == course_id]
    if search_term:
        result = [m for m in result if search_term.lower() in m["name"].lower()]
    if include and "items" in include:
        for m in result:
            m["items"] = deepcopy(MODULE_ITEMS.get(m["id"], []))
    result.sort(key=lambda x: x["position"])
    return result


@modules_router.get("/courses/{course_id}/modules/{module_id}", summary="Get a module")
async def get_module(
    course_id: int, module_id: int,
    include: Optional[List[str]] = Query(None),
    current_user=Depends(get_current_user),
):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    m = MODULES.get(module_id)
    if not m or m["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Module not found."}]})
    result = deepcopy(m)
    if include and "items" in include:
        result["items"] = deepcopy(MODULE_ITEMS.get(module_id, []))
    return result


@modules_router.post("/courses/{course_id}/modules", summary="Create a module")
async def create_module(course_id: int, body: dict, current_user=Depends(require_teacher)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    mdata = body.get("module", body)
    new_id = next_id("module")
    pos = max((m["position"] for m in MODULES.values() if m["course_id"] == course_id), default=0) + 1
    now = "2024-03-20T00:00:00Z"
    new_m = {
        "id": new_id, "course_id": course_id,
        "name": mdata.get("name", "New Module"),
        "position": mdata.get("position", pos),
        "unlock_at": mdata.get("unlock_at"),
        "require_sequential_progress": mdata.get("require_sequential_progress", False),
        "prerequisite_module_ids": mdata.get("prerequisite_module_ids", []),
        "items_count": 0,
        "items_url": f"/api/v1/courses/{course_id}/modules/{new_id}/items",
        "published": mdata.get("published", True),
        "workflow_state": "active",
        "state": "unlocked", "completed_at": None,
        "publish_final_grade": mdata.get("publish_final_grade", False),
    }
    MODULES[new_id] = new_m
    MODULE_ITEMS[new_id] = []
    return deepcopy(new_m)


@modules_router.put("/courses/{course_id}/modules/{module_id}", summary="Update a module")
async def update_module(course_id: int, module_id: int, body: dict, current_user=Depends(require_teacher)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    m = MODULES.get(module_id)
    if not m or m["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Module not found."}]})
    updates = body.get("module", body)
    m.update(updates)
    return deepcopy(m)


@modules_router.delete("/courses/{course_id}/modules/{module_id}", summary="Delete a module")
async def delete_module(course_id: int, module_id: int, current_user=Depends(require_teacher)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    m = MODULES.get(module_id)
    if not m or m["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Module not found."}]})
    del MODULES[module_id]
    return deepcopy(m)


@modules_router.get("/courses/{course_id}/modules/{module_id}/items", summary="List module items")
async def list_module_items(
    course_id: int, module_id: int,
    include: Optional[List[str]] = Query(None),
    search_term: Optional[str] = Query(None),
    current_user=Depends(get_current_user),
):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    if module_id not in MODULES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Module not found."}]})
    items = deepcopy(MODULE_ITEMS.get(module_id, []))
    if search_term:
        items = [i for i in items if search_term.lower() in i["title"].lower()]
    return items


@modules_router.get("/courses/{course_id}/modules/{module_id}/items/{item_id}", summary="Get a module item")
async def get_module_item(course_id: int, module_id: int, item_id: int, current_user=Depends(get_current_user)):
    items = MODULE_ITEMS.get(module_id, [])
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Module item not found."}]})
    return deepcopy(item)


@modules_router.post("/courses/{course_id}/modules/{module_id}/items", summary="Create a module item")
async def create_module_item(course_id: int, module_id: int, body: dict, current_user=Depends(require_teacher)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    m = MODULES.get(module_id)
    if not m or m["course_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Module not found."}]})
    idata = body.get("module_item", body)
    existing = MODULE_ITEMS.get(module_id, [])
    new_id = max((i["id"] for i in existing), default=0) + 1
    pos = max((i["position"] for i in existing), default=0) + 1
    new_item = {
        "id": new_id, "module_id": module_id,
        "position": idata.get("position", pos),
        "title": idata.get("title", "New Item"),
        "indent": idata.get("indent", 0),
        "type": idata.get("type", "Page"),
        "content_id": idata.get("content_id"),
        "url": idata.get("url"),
        "html_url": idata.get("html_url", f"/courses/{course_id}/modules/items/{new_id}"),
        "external_url": idata.get("external_url"),
        "new_tab": idata.get("new_tab", False),
        "published": idata.get("published", True),
        "completion_requirement": idata.get("completion_requirement"),
    }
    existing.append(new_item)
    MODULE_ITEMS[module_id] = existing
    m["items_count"] = len(existing)
    return deepcopy(new_item)


@modules_router.delete("/courses/{course_id}/modules/{module_id}/items/{item_id}", summary="Delete a module item")
async def delete_module_item(course_id: int, module_id: int, item_id: int, current_user=Depends(require_teacher)):
    items = MODULE_ITEMS.get(module_id, [])
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Module item not found."}]})
    MODULE_ITEMS[module_id] = [i for i in items if i["id"] != item_id]
    if module_id in MODULES:
        MODULES[module_id]["items_count"] = len(MODULE_ITEMS[module_id])
    return deepcopy(item)


# ═══════════════════════════════════════════════════════════════════════════════
# ANNOUNCEMENTS
# ═══════════════════════════════════════════════════════════════════════════════
announcements_router = APIRouter(prefix="/api/v1", tags=["Announcements"])


@announcements_router.get("/courses/{course_id}/discussion_topics", summary="List discussion topics (including announcements)")
async def list_discussion_topics(
    course_id: int,
    only_announcements: bool = Query(False),
    search_term: Optional[str] = Query(None),
    order_by: Optional[str] = Query("position"),
    current_user=Depends(get_current_user),
):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    if only_announcements:
        result = [deepcopy(a) for a in ANNOUNCEMENTS.values() if a["course_id"] == course_id]
    else:
        result = [deepcopy(t) for t in DISCUSSION_TOPICS.values() if t["course_id"] == course_id]
    if search_term:
        result = [t for t in result if search_term.lower() in t["title"].lower()]
    return result


@announcements_router.get("/courses/{course_id}/discussion_topics/{topic_id}", summary="Get a discussion topic")
async def get_discussion_topic(course_id: int, topic_id: int, current_user=Depends(get_current_user)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    topic = next((t for t in DISCUSSION_TOPICS.values() if t["id"] == topic_id and t["course_id"] == course_id), None)
    if not topic:
        topic = next((a for a in ANNOUNCEMENTS.values() if a["id"] == topic_id and a["course_id"] == course_id), None)
    if not topic:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Discussion topic not found."}]})
    return deepcopy(topic)


@announcements_router.post("/courses/{course_id}/discussion_topics", summary="Create a discussion topic or announcement")
async def create_discussion_topic(course_id: int, body: dict, current_user=Depends(require_teacher)):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})
    is_announcement = body.get("is_announcement", False)
    now = "2024-03-20T09:00:00Z"
    if is_announcement:
        new_id = next_id("announcement")
        new = {
            "id": new_id, "course_id": course_id,
            "title": body.get("title", "New Announcement"),
            "message": body.get("message", ""),
            "author": {"id": current_user["id"], "display_name": current_user["name"], "avatar_image_url": current_user.get("avatar_url")},
            "posted_at": now, "delayed_post_at": body.get("delayed_post_at"),
            "discussion_type": "side_comment", "pinned": body.get("pinned", False),
            "locked": body.get("locked", False), "position": new_id,
            "subscribed": True, "read_state": "unread", "unread_count": 0,
            "published": body.get("published", True),
            "allow_rating": False, "only_graders_can_rate": False, "sort_by_rating": False,
            "html_url": f"/courses/{course_id}/discussion_topics/{new_id}",
        }
        ANNOUNCEMENTS[new_id] = new
        return deepcopy(new)
    else:
        new_id = next_id("discussion")
        new = {
            "id": new_id, "course_id": course_id,
            "title": body.get("title", "New Discussion"),
            "message": body.get("message", ""),
            "author": {"id": current_user["id"], "display_name": current_user["name"]},
            "posted_at": now, "last_reply_at": None,
            "discussion_type": body.get("discussion_type", "threaded"),
            "pinned": body.get("pinned", False), "locked": body.get("locked", False),
            "position": new_id, "published": body.get("published", True),
            "subscribed": True, "assignment_id": body.get("assignment_id"),
            "delayed_post_at": body.get("delayed_post_at"),
            "lock_at": body.get("lock_at"),
            "podcast_enabled": False, "podcast_has_student_posts": False,
            "require_initial_post": body.get("require_initial_post", False),
            "user_can_see_posts": True,
            "discussion_subentry_count": 0, "unread_count": 0, "read_state": "read",
            "html_url": f"/courses/{course_id}/discussion_topics/{new_id}",
        }
        DISCUSSION_TOPICS[new_id] = new
        return deepcopy(new)
