# Canvas LMS Mock API

A **complete FastAPI mock** of the [Canvas LMS REST API](https://canvas.instructure.com/doc/api/index.html)  
using **in-memory mock data** — no database required. Built for front-end development and integration testing.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install fastapi uvicorn python-multipart

# 2. Start the server
uvicorn main:app --reload --port 8000

# 3. Open interactive docs
open http://localhost:8000/docs
```

---

## 🔐 Authentication

All `/api/v1/` endpoints require a Bearer token:

```
Authorization: Bearer <token>
```

### Pre-built Test Tokens

| Token | User | Role | Courses |
|---|---|---|---|
| `mock_access_token_teacher_1` | Alice Johnson | Teacher | CS101, CS201 |
| `mock_access_token_teacher_2` | Bob Martinez | Teacher | MATH301 |
| `mock_access_token_student_3` | Carol White | Student | CS101, MATH301 |

```bash
# Example
curl -H "Authorization: Bearer mock_access_token_teacher_1" \
     http://localhost:8000/api/v1/courses
```

---

## 🔑 OAuth 2.0 Flow

For testing full OAuth:

```bash
# Step 1 – Get auth code (OOB flow, no redirect needed)
GET /login/oauth2/auth
  ?client_id=mock_client_id_001
  &redirect_uri=urn:ietf:wg:oauth:2.0:oob
  &response_type=code
  &mock_user_id=1          # Simulate login as user 1 (Alice)

# Step 2 – Exchange for access token
POST /login/oauth2/token
  grant_type=authorization_code
  code=<code_from_step_1>
  client_id=mock_client_id_001
  client_secret=mock_client_secret_001
```

**Registered developer key:**  
- `client_id`: `mock_client_id_001`  
- `client_secret`: `mock_client_secret_001`

---

## 📦 Project Structure

```
canvas_mock_api/
├── main.py                  # FastAPI app, routers, CORS, error handlers
├── requirements.txt
├── data/
│   └── mock_data.py         # All in-memory data (users, courses, quizzes…)
├── core/
│   └── auth.py              # Bearer token validation, role guards
└── routers/
    ├── oauth.py             # OAuth 2.0 endpoints
    ├── courses.py           # Courses, enrollments, sections, tabs
    ├── quizzes.py           # Quizzes, questions, submissions, extensions
    ├── quiz_statistics.py   # Quiz aggregate statistics
    ├── rubrics.py           # Rubrics, associations, assessments
    ├── pages.py             # Wiki pages + revisions
    └── supplementary.py     # Assignments, Submissions, Users,
                             # Modules, Announcements, Discussions
```

---

## 📚 Included Endpoints

### OAuth
| Method | Path | Description |
|---|---|---|
| GET | `/login/oauth2/auth` | Authorization endpoint |
| POST | `/login/oauth2/token` | Token exchange / refresh |
| DELETE | `/login/oauth2/token` | Revoke token |
| GET | `/login/oauth2/token_info` | Introspect token |

### Courses
| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/courses` | List active courses |
| GET | `/api/v1/courses/:id` | Get a course |
| POST | `/api/v1/courses` | Create a course |
| PUT | `/api/v1/courses/:id` | Update a course |
| DELETE | `/api/v1/courses/:id` | Delete/conclude a course |
| GET | `/api/v1/courses/:id/enrollments` | List enrollments |
| POST | `/api/v1/courses/:id/enrollments` | Enroll a user |
| DELETE | `/api/v1/courses/:id/enrollments/:id` | Remove enrollment |
| GET | `/api/v1/courses/:id/students` | List students |
| GET | `/api/v1/courses/:id/users` | List all users |
| GET | `/api/v1/courses/:id/sections` | List sections |
| GET | `/api/v1/courses/:id/assignment_groups` | Assignment groups |
| GET | `/api/v1/courses/:id/grading_standards` | Grading standards |
| GET | `/api/v1/courses/:id/tabs` | Navigation tabs |

### Quizzes
| Method | Path | Description |
|---|---|---|
| GET/POST | `/api/v1/courses/:id/quizzes` | List / Create |
| GET/PUT/DELETE | `/api/v1/courses/:id/quizzes/:id` | Get / Update / Delete |
| GET/POST | `…/quizzes/:id/questions` | Questions |
| GET/PUT/DELETE | `…/quizzes/:id/questions/:id` | Single question |
| GET/POST | `…/quizzes/:id/submissions` | Submissions |
| PUT | `…/quizzes/:id/submissions/:id` | Complete submission |
| POST | `…/quizzes/:id/extensions` | Time extensions |
| GET | `…/quizzes/:id/ip_filters` | IP filters |

### Quiz Statistics
| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/courses/:id/quizzes/:id/statistics` | Full quiz stats |

### Rubrics
| Method | Path | Description |
|---|---|---|
| GET/POST | `/api/v1/courses/:id/rubrics` | List / Create |
| GET/PUT/DELETE | `/api/v1/courses/:id/rubrics/:id` | Get / Update / Delete |
| POST | `/api/v1/courses/:id/rubric_associations` | Associate rubric |
| PUT/DELETE | `/api/v1/courses/:id/rubric_associations/:id` | Manage association |
| GET/POST | `…/rubrics/:id/assessments` | Assessments |

### Pages (Wiki)
| Method | Path | Description |
|---|---|---|
| GET/POST | `/api/v1/courses/:id/pages` | List / Create |
| GET | `/api/v1/courses/:id/front_page` | Get front page |
| PUT | `/api/v1/courses/:id/front_page` | Update front page |
| GET/PUT/DELETE | `/api/v1/courses/:id/pages/:url` | Get / Update / Delete |
| GET | `…/pages/:url/revisions` | List revisions |
| GET | `…/pages/:url/revisions/latest` | Latest revision |
| GET | `…/pages/:url/revisions/:id` | Specific revision |
| POST | `…/pages/:url/revisions/:id` | Revert revision |

### Assignments
| Method | Path | Description |
|---|---|---|
| GET/POST | `/api/v1/courses/:id/assignments` | List / Create |
| GET/PUT/DELETE | `/api/v1/courses/:id/assignments/:id` | Get / Update / Delete |

### Submissions
| Method | Path | Description |
|---|---|---|
| GET | `…/assignments/:id/submissions` | List submissions |
| GET | `…/assignments/:id/submissions/:user_id` | Get submission |
| POST | `…/assignments/:id/submissions` | Submit assignment |
| PUT | `…/assignments/:id/submissions/:user_id` | Grade submission |

### Users
| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/users/self` | Current user |
| GET | `/api/v1/users/:id` | User by ID |
| GET | `/api/v1/users/self/enrollments` | My enrollments |
| GET | `/api/v1/users/self/courses` | My courses |
| GET | `/api/v1/accounts/1/users` | All users (teacher only) |

### Modules
| Method | Path | Description |
|---|---|---|
| GET/POST | `/api/v1/courses/:id/modules` | List / Create |
| GET/PUT/DELETE | `/api/v1/courses/:id/modules/:id` | Get / Update / Delete |
| GET/POST | `…/modules/:id/items` | Module items |
| GET/DELETE | `…/modules/:id/items/:id` | Item operations |

### Announcements & Discussions
| Method | Path | Description |
|---|---|---|
| GET | `…/discussion_topics?only_announcements=true` | Announcements |
| GET/POST | `/api/v1/courses/:id/discussion_topics` | Discussions |
| GET | `…/discussion_topics/:id` | Single topic |

---

## 🗂️ Mock Data Summary

| Resource | Count | Details |
|---|---|---|
| Users | 5 | Alice & Bob (teachers), Carol, David, Eva (students) |
| Courses | 3 | CS101 (Python), MATH301 (Calculus), CS201 (DSA) |
| Enrollments | 10 | Mixed across courses |
| Quizzes | 3 | With questions, submissions, and statistics |
| Quiz Questions | 7 | Multiple choice, true/false, short answer |
| Quiz Submissions | 3 | Completed, with scores |
| Quiz Statistics | 1 | For CS101 Python Basics quiz |
| Rubrics | 2 | Midterm Project + Linked List |
| Pages | 5 | Including 1 hidden draft |
| Modules | 3 | With prerequisite chain |
| Module Items | 9 | Pages, Quizzes, Assignments, External URLs |
| Assignments | 5 | Across all courses |
| Submissions | 5 | Some graded, some ungraded |
| Announcements | 2 | In CS101 |
| Discussion Topics | 2 | In CS101 |

---

## 🛠️ Extending the Mock

### Add a new resource

1. Add mock data to `data/mock_data.py`
2. Create a new router in `routers/`
3. Register it in `main.py`

### Seed different data

Edit the dictionaries in `data/mock_data.py`. All state is in-memory and resets on server restart.

### Add persistence (optional)

Replace the in-memory dicts with SQLite + SQLAlchemy, or just pickle/JSON file dumps on shutdown.

---

## 📝 Notes

- **Data resets** on every server restart (by design).
- The `Authorization: Bearer` header is required for all `/api/v1/` endpoints.
- Pagination headers (`Link: <url>; rel="next"`) are not implemented — all results are returned at once.
- The `mock_user_id` query param on `/login/oauth2/auth` is a **mock-only extension** to simulate any user logging in.
