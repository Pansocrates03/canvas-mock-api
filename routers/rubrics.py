"""
Canvas Mock API – Rubrics Endpoints
Implements: https://canvas.instructure.com/doc/api/rubrics.html
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from copy import deepcopy

from core.auth import get_current_user, require_teacher
from data.mock_data import COURSES, RUBRICS, RUBRIC_ASSESSMENTS, ASSIGNMENTS, next_id

router = APIRouter(prefix="/api/v1", tags=["Rubrics"])


def _check_course(course_id: int):
    if course_id not in COURSES:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Course not found."}]})


# ─── Rubrics ───────────────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/rubrics", summary="List rubrics for a course")
async def list_rubrics(
    course_id: int,
    include: Optional[List[str]] = Query(None, description="associations, association_data, assessed_students, graded_assessments, peer_assessments"),
    style: Optional[str] = Query(None, description="full, comments_only"),
    current_user=Depends(get_current_user),
):
    _check_course(course_id)
    result = [deepcopy(r) for r in RUBRICS.values() if r["context_id"] == course_id]
    for r in result:
        if not include or "assessments" not in include:
            r.pop("assessments", None)
        if not include or "associations" not in include:
            r.pop("associations", None)
    return result


@router.get("/courses/{course_id}/rubrics/{rubric_id}", summary="Get a single rubric")
async def get_rubric(
    course_id: int,
    rubric_id: int,
    include: Optional[List[str]] = Query(None),
    style: Optional[str] = Query(None),
    current_user=Depends(get_current_user),
):
    _check_course(course_id)
    rubric = RUBRICS.get(rubric_id)
    if not rubric or rubric["context_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Rubric not found."}]})
    r = deepcopy(rubric)
    if include and "assessments" in include:
        r["assessments"] = [a for a in RUBRIC_ASSESSMENTS.values() if a["rubric_id"] == rubric_id]
    if include and "associations" not in include:
        r.pop("associations", None)
    return r


@router.post("/courses/{course_id}/rubrics", summary="Create a rubric")
async def create_rubric(
    course_id: int,
    body: dict,
    current_user=Depends(require_teacher),
):
    _check_course(course_id)
    rdata = body.get("rubric", body)
    new_id = next_id("rubric")
    now = "2024-03-20T00:00:00Z"
    new_rubric = {
        "id": new_id,
        "title": rdata.get("title", "New Rubric"),
        "context_id": course_id,
        "context_type": "Course",
        "points_possible": sum(c.get("points", 0) for c in rdata.get("criteria", {}).values()) if isinstance(rdata.get("criteria"), dict) else 0,
        "reusable": rdata.get("reusable", False),
        "public": rdata.get("public", False),
        "read_only": False,
        "free_form_criterion_comments": rdata.get("free_form_criterion_comments", False),
        "hide_score_total": rdata.get("hide_score_total", False),
        "data": list(rdata.get("criteria", {}).values()) if isinstance(rdata.get("criteria"), dict) else [],
        "assessments": None,
        "associations": [],
        "created_at": now,
        "updated_at": now,
    }
    RUBRICS[new_id] = new_rubric
    return {"rubric": new_rubric, "rubric_association": None}


@router.put("/courses/{course_id}/rubrics/{rubric_id}", summary="Update a rubric")
async def update_rubric(
    course_id: int,
    rubric_id: int,
    body: dict,
    current_user=Depends(require_teacher),
):
    _check_course(course_id)
    rubric = RUBRICS.get(rubric_id)
    if not rubric or rubric["context_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Rubric not found."}]})
    rdata = body.get("rubric", body)
    updatable = ["title", "reusable", "public", "free_form_criterion_comments", "hide_score_total"]
    for k in updatable:
        if k in rdata:
            rubric[k] = rdata[k]
    if "criteria" in rdata:
        rubric["data"] = list(rdata["criteria"].values()) if isinstance(rdata["criteria"], dict) else rdata["criteria"]
    rubric["updated_at"] = "2024-03-20T00:00:00Z"
    return {"rubric": deepcopy(rubric)}


@router.delete("/courses/{course_id}/rubrics/{rubric_id}", summary="Delete a rubric")
async def delete_rubric(
    course_id: int,
    rubric_id: int,
    current_user=Depends(require_teacher),
):
    _check_course(course_id)
    rubric = RUBRICS.get(rubric_id)
    if not rubric or rubric["context_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Rubric not found."}]})
    del RUBRICS[rubric_id]
    return deepcopy(rubric)


# ─── Rubric Associations ───────────────────────────────────────────────────────

@router.post("/courses/{course_id}/rubric_associations", summary="Create a rubric association")
async def create_rubric_association(
    course_id: int,
    body: dict,
    current_user=Depends(require_teacher),
):
    _check_course(course_id)
    adata = body.get("rubric_association", body)
    rubric_id = adata.get("rubric_id")
    rubric = RUBRICS.get(rubric_id)
    if not rubric:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Rubric not found."}]})
    assoc_id = max((a["id"] for r in RUBRICS.values() for a in (r.get("associations") or [])), default=0) + 1
    new_assoc = {
        "id": assoc_id,
        "rubric_id": rubric_id,
        "association_id": adata.get("association_id"),
        "association_type": adata.get("association_type", "Assignment"),
        "use_for_grading": adata.get("use_for_grading", False),
        "summary_data": {},
        "purpose": adata.get("purpose", "grading"),
        "hide_score_total": adata.get("hide_score_total", False),
        "hide_points": adata.get("hide_points", False),
        "hide_outcome_results": adata.get("hide_outcome_results", False),
    }
    if rubric.get("associations") is None:
        rubric["associations"] = []
    rubric["associations"].append(new_assoc)
    return new_assoc


@router.put("/courses/{course_id}/rubric_associations/{rubric_association_id}", summary="Update a rubric association")
async def update_rubric_association(
    course_id: int,
    rubric_association_id: int,
    body: dict,
    current_user=Depends(require_teacher),
):
    _check_course(course_id)
    # Find the association across all rubrics
    for rubric in RUBRICS.values():
        for assoc in (rubric.get("associations") or []):
            if assoc["id"] == rubric_association_id:
                adata = body.get("rubric_association", body)
                assoc.update(adata)
                return assoc
    raise HTTPException(status_code=404, detail={"errors": [{"message": "Rubric association not found."}]})


@router.delete("/courses/{course_id}/rubric_associations/{rubric_association_id}", summary="Delete a rubric association")
async def delete_rubric_association(
    course_id: int,
    rubric_association_id: int,
    current_user=Depends(require_teacher),
):
    _check_course(course_id)
    for rubric in RUBRICS.values():
        associations = rubric.get("associations") or []
        for i, assoc in enumerate(associations):
            if assoc["id"] == rubric_association_id:
                removed = associations.pop(i)
                return removed
    raise HTTPException(status_code=404, detail={"errors": [{"message": "Rubric association not found."}]})


# ─── Rubric Assessments ────────────────────────────────────────────────────────

@router.get(
    "/courses/{course_id}/rubrics/{rubric_id}/assessments",
    summary="List rubric assessments",
)
async def list_rubric_assessments(
    course_id: int,
    rubric_id: int,
    current_user=Depends(get_current_user),
):
    _check_course(course_id)
    rubric = RUBRICS.get(rubric_id)
    if not rubric or rubric["context_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Rubric not found."}]})
    return [a for a in RUBRIC_ASSESSMENTS.values() if a["rubric_id"] == rubric_id]


@router.post(
    "/courses/{course_id}/rubrics/{rubric_id}/assessments",
    summary="Create or update a rubric assessment",
)
async def create_rubric_assessment(
    course_id: int,
    rubric_id: int,
    body: dict,
    current_user=Depends(require_teacher),
):
    _check_course(course_id)
    rubric = RUBRICS.get(rubric_id)
    if not rubric or rubric["context_id"] != course_id:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "Rubric not found."}]})
    adata = body.get("rubric_assessment", body)
    new_id = max(RUBRIC_ASSESSMENTS.keys(), default=0) + 1
    now = "2024-03-20T00:00:00Z"
    # Calculate total score from criteria
    data_list = adata.get("data", {})
    if isinstance(data_list, dict):
        data_list = list(data_list.values())
    total = sum(float(d.get("points", 0)) for d in data_list)
    assessment = {
        "id": new_id,
        "rubric_id": rubric_id,
        "rubric_association_id": adata.get("rubric_association_id"),
        "score": total,
        "artifact_type": adata.get("artifact_type", "Submission"),
        "artifact_id": adata.get("artifact_id"),
        "artifact_attempt": adata.get("artifact_attempt", 1),
        "assessor_id": current_user["id"],
        "user_id": adata.get("user_id"),
        "data": data_list,
        "created_at": now,
        "updated_at": now,
    }
    RUBRIC_ASSESSMENTS[new_id] = assessment
    return assessment
