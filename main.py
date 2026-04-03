"""
Canvas Mock API
═══════════════
A FastAPI application that replicates the Canvas LMS REST API using in-memory
mock data. Designed for front-end / integration development without needing
a real Canvas instance or database.

Quick Start
───────────
    pip install fastapi uvicorn
    uvicorn main:app --reload

Default Test Tokens
───────────────────
    Teacher (Alice, user 1): mock_access_token_teacher_1
    Teacher (Bob,   user 2): mock_access_token_teacher_2
    Student (Carol, user 3): mock_access_token_student_3

Usage example:
    curl -H "Authorization: Bearer mock_access_token_teacher_1" \
         http://localhost:8000/api/v1/courses
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os

# Make project root importable
sys.path.insert(0, os.path.dirname(__file__))

from routers.oauth       import router as oauth_router
from routers.courses     import router as courses_router
from routers.quizzes     import router as quizzes_router
from routers.quiz_statistics import router as quiz_stats_router
from routers.rubrics     import router as rubrics_router
from routers.pages       import router as pages_router
from routers.supplementary import (
    assignments_router,
    submissions_router,
    users_router,
    modules_router,
    announcements_router,
)

# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Canvas LMS Mock API",
    description="""
## Canvas LMS Mock API

A **full-fidelity mock** of the [Canvas LMS REST API](https://canvas.instructure.com/doc/api/index.html)
powered by FastAPI and in-memory data. Use this for front-end development and
integration testing without a real Canvas instance.

---

### Authentication

All `/api/v1/` endpoints require an `Authorization` header:

```
Authorization: Bearer <token>
```

**Pre-built test tokens:**

| Token | User | Role |
|---|---|---|
| `mock_access_token_teacher_1` | Alice Johnson | Teacher (CS101, CS201) |
| `mock_access_token_teacher_2` | Bob Martinez | Teacher (MATH301) |
| `mock_access_token_student_3` | Carol White | Student |

---

### OAuth Flow (for testing)

1. `GET /login/oauth2/auth?client_id=mock_client_id_001&redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=code&mock_user_id=1`
2. Copy the returned `code`
3. `POST /login/oauth2/token` with `grant_type=authorization_code&code=<code>&client_id=mock_client_id_001&client_secret=mock_client_secret_001`

---

### Included Resources

| Resource | Endpoints |
|---|---|
| **OAuth 2.0** | Authorization, Token, Revoke |
| **Courses** | CRUD, Enrollments, Students, Sections, Tabs |
| **Quizzes** | CRUD + Questions + Submissions + Extensions + IP Filters |
| **Quiz Statistics** | Aggregate + per-question stats |
| **Rubrics** | CRUD + Associations + Assessments |
| **Pages (Wiki)** | CRUD + Revisions + Front Page |
| **Assignments** | CRUD |
| **Submissions** | List, Get, Submit, Grade |
| **Users** | Profile, Self, Account list |
| **Modules** | CRUD + Module Items |
| **Announcements** | List, Get, Create |
| **Discussion Topics** | List, Get, Create |

---

### Mock Data Summary

- **3 Courses**: CS101, MATH301, CS201
- **5 Users**: 2 teachers (Alice, Bob), 3 students (Carol, David, Eva)
- **10 Enrollments** across the 3 courses
- **3 Quizzes** with questions, submissions, and statistics
- **2 Rubrics** with criteria and sample assessments
- **5 Pages** (including draft/hidden)
- **3 Modules** with items and prerequisites
- **5 Assignments** with some graded submissions
""",
    version="1.0.0",
    contact={
        "name": "Canvas Mock API",
        "url": "https://canvas.instructure.com/doc/api/",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {"name": "OAuth",             "description": "OAuth 2.0 authorization endpoints"},
        {"name": "Courses",           "description": "Course management"},
        {"name": "Quizzes",           "description": "Quizzes, questions, submissions, extensions"},
        {"name": "Quiz Statistics",   "description": "Aggregate quiz statistics"},
        {"name": "Rubrics",           "description": "Rubrics and rubric assessments"},
        {"name": "Pages",             "description": "Wiki/course pages and revisions"},
        {"name": "Assignments",       "description": "Assignment management"},
        {"name": "Submissions",       "description": "Assignment submissions and grading"},
        {"name": "Users",             "description": "User profiles and enrollments"},
        {"name": "Modules",           "description": "Course modules and module items"},
        {"name": "Announcements",     "description": "Announcements and discussion topics"},
    ],
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Global error handler to mirror Canvas's error format ─────────────────────
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"errors": [{"type": "not_found", "message": "The specified resource does not exist."}]},
    )

@app.exception_handler(405)
async def method_not_allowed_handler(request: Request, exc):
    return JSONResponse(
        status_code=405,
        content={"errors": [{"type": "method_not_allowed", "message": "Method Not Allowed"}]},
    )

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(oauth_router)
app.include_router(courses_router)
app.include_router(quizzes_router)
app.include_router(quiz_stats_router)
app.include_router(rubrics_router)
app.include_router(pages_router)
app.include_router(assignments_router)
app.include_router(submissions_router)
app.include_router(users_router)
app.include_router(modules_router)
app.include_router(announcements_router)

# ─── Root / Health ────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    return {
        "name": "Canvas Mock API",
        "version": "1.0.0",
        "description": "FastAPI-powered mock of the Canvas LMS REST API",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "quick_test_tokens": {
            "teacher_alice": "mock_access_token_teacher_1",
            "teacher_bob":   "mock_access_token_teacher_2",
            "student_carol": "mock_access_token_student_3",
        },
        "example_request": "curl -H 'Authorization: Bearer mock_access_token_teacher_1' http://localhost:8000/api/v1/courses",
    }


@app.get("/api/v1", include_in_schema=False)
async def api_root():
    return {"status": "ok", "message": "Canvas Mock API v1 is running."}


# ─── Run directly ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
