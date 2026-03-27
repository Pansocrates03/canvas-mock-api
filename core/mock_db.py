from datetime import datetime

# Se actualizó el usuario simulado para tu entorno local
MOCK_USERS = {"1": {"id": 1, "name": "Esteban", "login_id": "A00836286@tec.mx"}}

MOCK_COURSES = [
    {
        "id": 1,
        "uuid": "WvAHhY5FINzq5IyRIJybGeiXyFkG3SqHUPb7jZY5",
        "name": "Desarrollo de Software Moderno",
        "course_code": "CS-101",
        "workflow_state": "available",
        "account_id": 81259,
        "root_account_id": 81259,
        "enrollment_term_id": 34,
        "created_at": datetime.fromisoformat("2023-08-01T00:00:00-06:00"),
        "default_view": "modules",
        "apply_assignment_group_weights": True,
        "is_public": False,
        "is_public_to_auth_users": False,
        "public_syllabus": False,
        "public_syllabus_to_auth": False,
        "storage_quota_mb": 500,
        "storage_quota_used_mb": 150.5,
        "hide_final_grades": False,
        "license": "private",
        "allow_student_assignment_edits": False,
        "allow_wiki_comments": False,
        "allow_student_forum_attachments": True,
        "restrict_enrollments_to_course_dates": False,
        "time_zone": "America/Mexico_City"
    }
]

MOCK_ENROLLMENTS = [
    {
        "id": 1001,
        "course_id": 1,
        "course_section_id": 201,
        "enrollment_state": "active",
        "limit_privileges_to_course_section": False,
        "root_account_id": 81259,
        "type": "StudentEnrollment",
        "user_id": 1,
        "role": "StudentEnrollment",
        "role_id": 3,
        "created_at": datetime.fromisoformat("2023-08-01T10:00:00-06:00"),
        "updated_at": datetime.fromisoformat("2023-08-15T10:00:00-06:00"),
        "total_activity_time": 86400,
        "html_url": "https://canvas.mock/courses/1/users/1",
        "grades": {
            "html_url": "https://canvas.mock/courses/1/grades/1",
            "current_score": 92.5,
            "current_grade": "A-",
            "final_score": 92.5,
            "final_grade": "A-"
        },
        "user": MOCK_USERS["1"]
    }
]

MOCK_ASSIGNMENTS = [
    {
        "id": 501,
        "course_id": 1,
        "name": "Diagrama ER de la Base de Datos",
        "description": "<p>Sube el diagrama entidad-relación del proyecto en formato PDF.</p>",
        "due_at": datetime.fromisoformat("2023-09-15T23:59:59-06:00"),
        "unlock_at": datetime.fromisoformat("2023-09-01T00:00:00-06:00"),
        "lock_at": None,
        "points_possible": 100.0,
        "submission_types": ["online_upload"],
        "allowed_extensions": ["pdf", "png"],
        "grading_type": "points",
        "published": True,
        "html_url": "https://canvas.mock/courses/1/assignments/501"
    }
]

MOCK_QUIZZES = [
    {"id": 101, "course_id": 1, "title": "Examen Parcial 1"}
]

MOCK_QUIZ_STATS = [
    {"id": 1, "quiz_id": 101, "submission_statistics": {"score_average": 85.5}}
]

MOCK_FILES = [
    {
        "id": 569,
        "folder_id": 4207,
        "display_name": "file.txt",
        "filename": "file.txt",
        "content-type": "text/plain",
        "url": "http://www.example.com/files/569/download?download_frd=1",
        "size": 43451,
        "created_at": "2012-07-06T14:58:50Z",
        "updated_at": "2012-07-06T14:58:50Z",
        "unlock_at": "2012-07-07T14:58:50Z",
        "locked": False,
        "hidden": False,
        "lock_at": "2012-07-20T14:58:50Z",
        "hidden_for_user": False,
        "visibility_level": "course",
        "thumbnail_url": None,
        "modified_at": "2012-07-06T14:58:50Z",
        "mime_class": "html",
        "media_entry_id": "m-3z31gfpPf129dD3sSDF85SwSDFnwe",
        "locked_for_user": False,
        "lock_info": None,
        "lock_explanation": "This assignment is locked until September 1 at 12:00am",
        "preview_url": None
    }
]