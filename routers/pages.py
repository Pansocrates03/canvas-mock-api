"""
Canvas Mock API – Pages (Wiki Pages) Endpoints
Implements: https://canvas.instructure.com/doc/api/pages.html
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from copy import deepcopy
import re

from core.auth import get_current_user, require_teacher
from data.mock_data import COURSES, PAGES, USERS, next_id

router = APIRouter(prefix="/api/v1", tags=["Pages"])


def _check_course(course_id: int):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})


def _to_url_slug(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s_]+", "-", slug)
    return slug.strip("-")


def _page_for_student(page: dict) -> bool:
    """Return True if page should be visible to students."""
    return page.get("published", False) and not page.get("hide_from_students", False)


# ─── List Pages ────────────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/pages", summary="List pages in a course")
async def list_pages(
    course_id: int,
    sort: Optional[str] = Query("title", description="Sort field: title, created_at, updated_at"),
    order: Optional[str] = Query("asc", description="Sort order: asc, desc"),
    search_term: Optional[str] = Query(None, description="Filter by title"),
    published: Optional[bool] = Query(None, description="Filter by published state"),
    current_user=Depends(get_current_user),
):
    _check_course(course_id)
    is_teacher = "teacher" in current_user.get("roles", [])
    pages = [deepcopy(p) for p in PAGES.values() if p["course_id"] == course_id]

    if not is_teacher:
        pages = [p for p in pages if _page_for_student(p)]

    if search_term:
        pages = [p for p in pages if search_term.lower() in p["title"].lower()]

    if published is not None:
        pages = [p for p in pages if p.get("published") == published]

    # Strip body from list view (Canvas returns page objects without body)
    for p in pages:
        p.pop("body", None)

    reverse = order == "desc"
    pages.sort(key=lambda x: x.get(sort, ""), reverse=reverse)
    return pages


# ─── Get Front Page ────────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/front_page", summary="Get the front page of a course")
async def get_front_page(course_id: int, current_user=Depends(get_current_user)):
    _check_course(course_id)
    is_teacher = "teacher" in current_user.get("roles", [])
    front = next(
        (p for p in PAGES.values() if p["course_id"] == course_id and p.get("front_page")),
        None,
    )
    if not front:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "No front page has been set."}]})
    if not is_teacher and not _page_for_student(front):
        raise HTTPException(status_code=403, detail={"errors": [{"message": "Unauthorized."}]})
    return deepcopy(front)


@router.put("/courses/{course_id}/front_page", summary="Update the front page")
async def update_front_page(course_id: int, body: dict, current_user=Depends(require_teacher)):
    _check_course(course_id)
    wdata = body.get("wiki_page", body)
    front = next((p for p in PAGES.values() if p["course_id"] == course_id and p.get("front_page")), None)
    if not front:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "No front page set."}]})
    front.update({k: v for k, v in wdata.items() if k in front})
    front["updated_at"] = "2024-03-20T00:00:00Z"
    return deepcopy(front)


# ─── Get / Create / Update / Delete individual pages ──────────────────────────

@router.get("/courses/{course_id}/pages/{url_or_id}", summary="Get a page by url or id")
async def get_page(course_id: int, url_or_id: str, current_user=Depends(get_current_user)):
    _check_course(course_id)
    is_teacher = "teacher" in current_user.get("roles", [])
    page = _find_page(course_id, url_or_id)
    if not is_teacher and not _page_for_student(page):
        raise HTTPException(status_code=403, detail={"errors": [{"message": "Page is locked or not published."}]})
    return deepcopy(page)


@router.post("/courses/{course_id}/pages", summary="Create a page")
async def create_page(course_id: int, body: dict, current_user=Depends(require_teacher)):
    _check_course(course_id)
    wdata = body.get("wiki_page", body)
    title = wdata.get("title", "New Page")
    url = _to_url_slug(title)
    # Ensure unique URL
    existing_urls = {p["url"] for p in PAGES.values() if p["course_id"] == course_id}
    base, counter = url, 2
    while url in existing_urls:
        url = f"{base}-{counter}"
        counter += 1
    new_id = next_id("page")
    now = "2024-03-20T00:00:00Z"
    new_page = {
        "page_id": new_id,
        "url": url,
        "title": title,
        "course_id": course_id,
        "created_at": now,
        "updated_at": now,
        "hide_from_students": wdata.get("hide_from_students", False),
        "editing_roles": wdata.get("editing_roles", "teachers"),
        "last_edited_by": {
            "id": current_user["id"],
            "display_name": current_user["name"],
            "avatar_image_url": current_user.get("avatar_url"),
            "html_url": f"/users/{current_user['id']}",
        },
        "body": wdata.get("body", ""),
        "published": wdata.get("published", False),
        "front_page": wdata.get("front_page", False),
        "locked_for_user": False,
        "lock_info": None,
        "lock_explanation": None,
    }
    PAGES[new_id] = new_page
    return deepcopy(new_page)


@router.put("/courses/{course_id}/pages/{url_or_id}", summary="Update a page")
async def update_page(course_id: int, url_or_id: str, body: dict, current_user=Depends(require_teacher)):
    _check_course(course_id)
    page = _find_page(course_id, url_or_id)
    wdata = body.get("wiki_page", body)

    # If setting as front page, unset others
    if wdata.get("front_page"):
        for p in PAGES.values():
            if p["course_id"] == course_id and p["page_id"] != page["page_id"]:
                p["front_page"] = False

    updatable = ["title", "body", "published", "front_page", "editing_roles", "hide_from_students"]
    for k in updatable:
        if k in wdata:
            page[k] = wdata[k]

    if "title" in wdata:
        page["url"] = _to_url_slug(wdata["title"])

    page["updated_at"] = "2024-03-20T00:00:00Z"
    page["last_edited_by"] = {
        "id": current_user["id"],
        "display_name": current_user["name"],
        "avatar_image_url": current_user.get("avatar_url"),
        "html_url": f"/users/{current_user['id']}",
    }
    return deepcopy(page)


@router.delete("/courses/{course_id}/pages/{url_or_id}", summary="Delete a page")
async def delete_page(course_id: int, url_or_id: str, current_user=Depends(require_teacher)):
    _check_course(course_id)
    page = _find_page(course_id, url_or_id)
    if page.get("front_page"):
        raise HTTPException(status_code=400, detail={"errors": [{"message": "The front page cannot be deleted."}]})
    del PAGES[page["page_id"]]
    return deepcopy(page)


# ─── Page Revisions ────────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/pages/{url_or_id}/revisions", summary="List page revisions")
async def list_page_revisions(course_id: int, url_or_id: str, current_user=Depends(get_current_user)):
    _check_course(course_id)
    page = _find_page(course_id, url_or_id)
    # Mock: return a single revision (the current state)
    return [
        {
            "revision_id": 1,
            "created_at": page["created_at"],
            "updated_at": page["updated_at"],
            "latest": True,
            "edited_by": page.get("last_edited_by"),
            "url": page["url"],
            "title": page["title"],
            "body": page.get("body"),
        }
    ]


@router.get("/courses/{course_id}/pages/{url_or_id}/revisions/latest", summary="Get the latest page revision")
async def get_latest_page_revision(course_id: int, url_or_id: str, current_user=Depends(get_current_user)):
    _check_course(course_id)
    page = _find_page(course_id, url_or_id)
    return {
        "revision_id": 1,
        "created_at": page["created_at"],
        "updated_at": page["updated_at"],
        "latest": True,
        "edited_by": page.get("last_edited_by"),
        "url": page["url"],
        "title": page["title"],
        "body": page.get("body"),
    }


@router.get("/courses/{course_id}/pages/{url_or_id}/revisions/{revision_id}", summary="Get a specific page revision")
async def get_page_revision(course_id: int, url_or_id: str, revision_id: int, current_user=Depends(get_current_user)):
    _check_course(course_id)
    page = _find_page(course_id, url_or_id)
    if revision_id != 1:
        raise HTTPException(status_code=404, detail={"errors": [{"message": f"Revision {revision_id} not found (only revision 1 exists in mock)."}]})
    return {
        "revision_id": 1,
        "created_at": page["created_at"],
        "updated_at": page["updated_at"],
        "latest": True,
        "edited_by": page.get("last_edited_by"),
        "url": page["url"],
        "title": page["title"],
        "body": page.get("body"),
    }


@router.post("/courses/{course_id}/pages/{url_or_id}/revisions/{revision_id}", summary="Revert to a page revision")
async def revert_page_revision(course_id: int, url_or_id: str, revision_id: int, current_user=Depends(require_teacher)):
    _check_course(course_id)
    page = _find_page(course_id, url_or_id)
    if revision_id != 1:
        raise HTTPException(status_code=404, detail={"errors": [{"message": f"Revision {revision_id} not found."}]})
    return deepcopy(page)


# ─── Helper ────────────────────────────────────────────────────────────────────

def _find_page(course_id: int, url_or_id: str) -> dict:
    # Try numeric ID first
    try:
        pid = int(url_or_id)
        page = PAGES.get(pid)
        if page and page["course_id"] == course_id:
            return page
    except ValueError:
        pass
    # Try URL slug
    page = next((p for p in PAGES.values() if p["course_id"] == course_id and p["url"] == url_or_id), None)
    if not page:
        raise HTTPException(status_code=404, detail={"errors": [{"message": f"Page '{url_or_id}' not found in course {course_id}."}]})
    return page
