"""
Canvas Mock API - Mock Data Store
All data lives here in memory, simulating a real Canvas instance.
"""
from datetime import datetime, timedelta
import uuid

# ─────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────
USERS = {
    1: {
        "id": 1,
        "name": "Alice Johnson",
        "sortable_name": "Johnson, Alice",
        "short_name": "Alice J.",
        "sis_user_id": "SIS001",
        "login_id": "alice@university.edu",
        "email": "alice@university.edu",
        "avatar_url": "https://i.pravatar.cc/150?u=alice",
        "locale": "en",
        "pronouns": "she/her",
        "time_zone": "America/Chicago",
        "bio": "Computer Science student",
        "created_at": "2023-01-10T08:00:00Z",
        "updated_at": "2024-01-10T08:00:00Z",
        "roles": ["teacher"],
    },
    2: {
        "id": 2,
        "name": "Bob Martinez",
        "sortable_name": "Martinez, Bob",
        "short_name": "Bob M.",
        "sis_user_id": "SIS002",
        "login_id": "bob@university.edu",
        "email": "bob@university.edu",
        "avatar_url": "https://i.pravatar.cc/150?u=bob",
        "locale": "en",
        "pronouns": "he/him",
        "time_zone": "America/Chicago",
        "bio": "Mathematics professor",
        "created_at": "2023-01-15T08:00:00Z",
        "updated_at": "2024-01-15T08:00:00Z",
        "roles": ["teacher"],
    },
    3: {
        "id": 3,
        "name": "Carol White",
        "sortable_name": "White, Carol",
        "short_name": "Carol W.",
        "sis_user_id": "SIS003",
        "login_id": "carol@university.edu",
        "email": "carol@university.edu",
        "avatar_url": "https://i.pravatar.cc/150?u=carol",
        "locale": "en",
        "pronouns": None,
        "time_zone": "America/Chicago",
        "bio": "First year student",
        "created_at": "2023-08-20T08:00:00Z",
        "updated_at": "2024-01-20T08:00:00Z",
        "roles": ["student"],
    },
    4: {
        "id": 4,
        "name": "David Lee",
        "sortable_name": "Lee, David",
        "short_name": "David L.",
        "sis_user_id": "SIS004",
        "login_id": "david@university.edu",
        "email": "david@university.edu",
        "avatar_url": "https://i.pravatar.cc/150?u=david",
        "locale": "en",
        "pronouns": "he/him",
        "time_zone": "America/Chicago",
        "bio": "Second year student",
        "created_at": "2023-08-20T08:00:00Z",
        "updated_at": "2024-01-20T08:00:00Z",
        "roles": ["student"],
    },
    5: {
        "id": 5,
        "name": "Eva Chen",
        "sortable_name": "Chen, Eva",
        "short_name": "Eva C.",
        "sis_user_id": "SIS005",
        "login_id": "eva@university.edu",
        "email": "eva@university.edu",
        "avatar_url": "https://i.pravatar.cc/150?u=eva",
        "locale": "en",
        "pronouns": "she/her",
        "time_zone": "America/Chicago",
        "bio": "Third year student",
        "created_at": "2022-08-20T08:00:00Z",
        "updated_at": "2024-01-20T08:00:00Z",
        "roles": ["student"],
    },
}

# ─────────────────────────────────────────────
# OAUTH TOKENS
# ─────────────────────────────────────────────
OAUTH_CODES = {}   # authorization_code -> user_id
OAUTH_TOKENS = {
    "mock_access_token_teacher_1": {
        "user_id": 1,
        "scope": "*",
        "expires_in": 3600,
        "token_type": "Bearer",
    },
    "mock_access_token_teacher_2": {
        "user_id": 2,
        "scope": "*",
        "expires_in": 3600,
        "token_type": "Bearer",
    },
    "mock_access_token_student_3": {
        "user_id": 3,
        "scope": "url:GET|/api/v1/courses",
        "expires_in": 3600,
        "token_type": "Bearer",
    },
}
REFRESH_TOKENS = {
    "mock_refresh_token_1": {"user_id": 1, "access_token": "mock_access_token_teacher_1"},
    "mock_refresh_token_2": {"user_id": 2, "access_token": "mock_access_token_teacher_2"},
}

# ─────────────────────────────────────────────
# ACCOUNTS
# ─────────────────────────────────────────────
ACCOUNTS = {
    1: {
        "id": 1,
        "name": "University of Mock",
        "uuid": "mock-account-uuid-0001",
        "parent_account_id": None,
        "root_account_id": 1,
        "default_storage_quota_mb": 500,
        "default_user_storage_quota_mb": 50,
        "default_group_storage_quota_mb": 50,
        "default_time_zone": "America/Chicago",
        "sis_account_id": "ROOT",
        "lti_guid": "mock.university.edu",
        "workflow_state": "active",
    }
}

# ─────────────────────────────────────────────
# COURSES
# ─────────────────────────────────────────────
COURSES = {
    1: {
        "id": 1,
        "name": "Introduction to Python",
        "course_code": "CS101",
        "uuid": "abc123-python-course",
        "sis_course_id": "CS101-2024",
        "integration_id": None,
        "account_id": 1,
        "root_account_id": 1,
        "enrollment_term_id": 1,
        "grading_standard_id": None,
        "start_at": "2024-01-15T00:00:00Z",
        "end_at": "2024-05-15T00:00:00Z",
        "created_at": "2023-12-01T00:00:00Z",
        "updated_at": "2024-01-10T00:00:00Z",
        "locale": "en",
        "enrollments": None,
        "total_students": 3,
        "calendar": {"ics": "https://mock.university.edu/feeds/calendars/course_abc123.ics"},
        "default_view": "modules",
        "syllabus_body": "<p>Welcome to Introduction to Python! This course covers...</p>",
        "needs_grading_count": 5,
        "term": {"id": 1, "name": "Spring 2024"},
        "public_syllabus": True,
        "public_syllabus_to_auth": True,
        "storage_quota_mb": 500,
        "is_public": False,
        "is_public_to_auth_users": False,
        "hide_final_grades": False,
        "license": "private",
        "allow_student_assignment_edits": False,
        "allow_wiki_comments": False,
        "allow_student_forum_attachments": True,
        "open_enrollment": False,
        "self_enrollment": False,
        "restrict_enrollments_to_course_dates": False,
        "course_format": "on_campus",
        "workflow_state": "available",
        "restrict_student_past_view": False,
        "restrict_student_future_view": False,
        "show_announcements_on_home_page": True,
        "home_page_announcement_limit": 3,
        "blueprint": False,
        "time_zone": "America/Chicago",
        "teacher_id": 1,
    },
    2: {
        "id": 2,
        "name": "Advanced Calculus",
        "course_code": "MATH301",
        "uuid": "def456-calculus-course",
        "sis_course_id": "MATH301-2024",
        "integration_id": None,
        "account_id": 1,
        "root_account_id": 1,
        "enrollment_term_id": 1,
        "grading_standard_id": None,
        "start_at": "2024-01-15T00:00:00Z",
        "end_at": "2024-05-15T00:00:00Z",
        "created_at": "2023-12-01T00:00:00Z",
        "updated_at": "2024-01-10T00:00:00Z",
        "locale": "en",
        "enrollments": None,
        "total_students": 2,
        "calendar": {"ics": "https://mock.university.edu/feeds/calendars/course_def456.ics"},
        "default_view": "feed",
        "syllabus_body": "<p>Advanced Calculus covers integration, differentiation...</p>",
        "needs_grading_count": 2,
        "term": {"id": 1, "name": "Spring 2024"},
        "public_syllabus": False,
        "public_syllabus_to_auth": True,
        "storage_quota_mb": 500,
        "is_public": False,
        "is_public_to_auth_users": False,
        "hide_final_grades": False,
        "license": "private",
        "allow_student_assignment_edits": False,
        "allow_wiki_comments": True,
        "allow_student_forum_attachments": True,
        "open_enrollment": False,
        "self_enrollment": False,
        "restrict_enrollments_to_course_dates": True,
        "course_format": "on_campus",
        "workflow_state": "available",
        "restrict_student_past_view": False,
        "restrict_student_future_view": False,
        "show_announcements_on_home_page": False,
        "home_page_announcement_limit": 3,
        "blueprint": False,
        "time_zone": "America/Chicago",
        "teacher_id": 2,
    },
    3: {
        "id": 3,
        "name": "Data Structures & Algorithms",
        "course_code": "CS201",
        "uuid": "ghi789-dsa-course",
        "sis_course_id": "CS201-2024",
        "integration_id": None,
        "account_id": 1,
        "root_account_id": 1,
        "enrollment_term_id": 1,
        "grading_standard_id": None,
        "start_at": "2024-01-15T00:00:00Z",
        "end_at": "2024-05-15T00:00:00Z",
        "created_at": "2023-12-01T00:00:00Z",
        "updated_at": "2024-01-10T00:00:00Z",
        "locale": "en",
        "enrollments": None,
        "total_students": 2,
        "calendar": {"ics": "https://mock.university.edu/feeds/calendars/course_ghi789.ics"},
        "default_view": "modules",
        "syllabus_body": "<p>Data Structures & Algorithms teaches core CS fundamentals...</p>",
        "needs_grading_count": 8,
        "term": {"id": 1, "name": "Spring 2024"},
        "public_syllabus": True,
        "public_syllabus_to_auth": True,
        "storage_quota_mb": 500,
        "is_public": False,
        "is_public_to_auth_users": False,
        "hide_final_grades": False,
        "license": "public_domain",
        "allow_student_assignment_edits": False,
        "allow_wiki_comments": False,
        "allow_student_forum_attachments": True,
        "open_enrollment": False,
        "self_enrollment": False,
        "restrict_enrollments_to_course_dates": False,
        "course_format": "online",
        "workflow_state": "available",
        "restrict_student_past_view": False,
        "restrict_student_future_view": False,
        "show_announcements_on_home_page": True,
        "home_page_announcement_limit": 5,
        "blueprint": False,
        "time_zone": "America/Chicago",
        "teacher_id": 1,
    },
}

# ─────────────────────────────────────────────
# ENROLLMENTS
# ─────────────────────────────────────────────
ENROLLMENTS = {
    1:  {"id": 1,  "course_id": 1, "user_id": 1, "type": "TeacherEnrollment", "enrollment_state": "active", "role": "TeacherEnrollment", "role_id": 4, "created_at": "2023-12-01T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z", "grades": None, "html_url": "/courses/1/users/1", "last_activity_at": "2024-03-01T10:00:00Z"},
    2:  {"id": 2,  "course_id": 1, "user_id": 3, "type": "StudentEnrollment", "enrollment_state": "active", "role": "StudentEnrollment", "role_id": 3, "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z", "grades": {"current_score": 88.5, "final_score": 88.5, "current_grade": "B+", "final_grade": "B+"}, "html_url": "/courses/1/users/3", "last_activity_at": "2024-03-15T14:00:00Z"},
    3:  {"id": 3,  "course_id": 1, "user_id": 4, "type": "StudentEnrollment", "enrollment_state": "active", "role": "StudentEnrollment", "role_id": 3, "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z", "grades": {"current_score": 72.0, "final_score": 72.0, "current_grade": "C", "final_grade": "C"}, "html_url": "/courses/1/users/4", "last_activity_at": "2024-03-14T09:00:00Z"},
    4:  {"id": 4,  "course_id": 1, "user_id": 5, "type": "StudentEnrollment", "enrollment_state": "active", "role": "StudentEnrollment", "role_id": 3, "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z", "grades": {"current_score": 95.0, "final_score": 95.0, "current_grade": "A", "final_grade": "A"}, "html_url": "/courses/1/users/5", "last_activity_at": "2024-03-16T11:00:00Z"},
    5:  {"id": 5,  "course_id": 2, "user_id": 2, "type": "TeacherEnrollment", "enrollment_state": "active", "role": "TeacherEnrollment", "role_id": 4, "created_at": "2023-12-01T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z", "grades": None, "html_url": "/courses/2/users/2", "last_activity_at": "2024-03-10T10:00:00Z"},
    6:  {"id": 6,  "course_id": 2, "user_id": 3, "type": "StudentEnrollment", "enrollment_state": "active", "role": "StudentEnrollment", "role_id": 3, "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z", "grades": {"current_score": 78.0, "final_score": 78.0, "current_grade": "C+", "final_grade": "C+"}, "html_url": "/courses/2/users/3", "last_activity_at": "2024-03-12T15:00:00Z"},
    7:  {"id": 7,  "course_id": 2, "user_id": 4, "type": "StudentEnrollment", "enrollment_state": "active", "role": "StudentEnrollment", "role_id": 3, "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z", "grades": {"current_score": 91.0, "final_score": 91.0, "current_grade": "A-", "final_grade": "A-"}, "html_url": "/courses/2/users/4", "last_activity_at": "2024-03-13T13:00:00Z"},
    8:  {"id": 8,  "course_id": 3, "user_id": 1, "type": "TeacherEnrollment", "enrollment_state": "active", "role": "TeacherEnrollment", "role_id": 4, "created_at": "2023-12-01T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z", "grades": None, "html_url": "/courses/3/users/1", "last_activity_at": "2024-03-16T10:00:00Z"},
    9:  {"id": 9,  "course_id": 3, "user_id": 4, "type": "StudentEnrollment", "enrollment_state": "active", "role": "StudentEnrollment", "role_id": 3, "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z", "grades": {"current_score": 85.5, "final_score": 85.5, "current_grade": "B", "final_grade": "B"}, "html_url": "/courses/3/users/4", "last_activity_at": "2024-03-15T16:00:00Z"},
    10: {"id": 10, "course_id": 3, "user_id": 5, "type": "StudentEnrollment", "enrollment_state": "active", "role": "StudentEnrollment", "role_id": 3, "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z", "grades": {"current_score": 97.0, "final_score": 97.0, "current_grade": "A+", "final_grade": "A+"}, "html_url": "/courses/3/users/5", "last_activity_at": "2024-03-16T08:00:00Z"},
}

# ─────────────────────────────────────────────
# SECTIONS
# ─────────────────────────────────────────────
SECTIONS = {
    1: {"id": 1, "course_id": 1, "name": "Section 001", "sis_section_id": "CS101-S1", "integration_id": None, "start_at": "2024-01-15T00:00:00Z", "end_at": "2024-05-15T00:00:00Z", "created_at": "2023-12-01T00:00:00Z", "restrict_enrollments_to_section_dates": False, "nonxlist_course_id": None, "total_students": 3},
    2: {"id": 2, "course_id": 2, "name": "Section 001", "sis_section_id": "MATH301-S1", "integration_id": None, "start_at": "2024-01-15T00:00:00Z", "end_at": "2024-05-15T00:00:00Z", "created_at": "2023-12-01T00:00:00Z", "restrict_enrollments_to_section_dates": False, "nonxlist_course_id": None, "total_students": 2},
    3: {"id": 3, "course_id": 3, "name": "Section 001", "sis_section_id": "CS201-S1", "integration_id": None, "start_at": "2024-01-15T00:00:00Z", "end_at": "2024-05-15T00:00:00Z", "created_at": "2023-12-01T00:00:00Z", "restrict_enrollments_to_section_dates": False, "nonxlist_course_id": None, "total_students": 2},
    4: {"id": 4, "course_id": 3, "name": "Section 002 (Online)", "sis_section_id": "CS201-S2", "integration_id": None, "start_at": "2024-01-15T00:00:00Z", "end_at": "2024-05-15T00:00:00Z", "created_at": "2023-12-01T00:00:00Z", "restrict_enrollments_to_section_dates": False, "nonxlist_course_id": None, "total_students": 0},
}

# ─────────────────────────────────────────────
# ASSIGNMENTS
# ─────────────────────────────────────────────
ASSIGNMENTS = {
    1: {
        "id": 1, "course_id": 1, "name": "Hello World Program", "description": "<p>Write a Python program that prints Hello World and your name.</p>",
        "due_at": "2024-02-01T23:59:00Z", "lock_at": "2024-02-02T23:59:00Z", "unlock_at": "2024-01-15T00:00:00Z",
        "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z",
        "points_possible": 100.0, "grading_type": "points", "submission_types": ["online_upload", "online_text_entry"],
        "has_submitted_submissions": True, "published": True, "only_visible_to_overrides": False,
        "assignment_group_id": 1, "position": 1, "peer_reviews": False, "automatic_peer_reviews": False,
        "grade_group_students_individually": False, "anonymous_submissions": False,
        "omit_from_final_grade": False, "moderated_grading": False, "rubric_id": None,
        "html_url": "/courses/1/assignments/1", "needs_grading_count": 1,
    },
    2: {
        "id": 2, "course_id": 1, "name": "Midterm Project - Calculator App", "description": "<p>Build a calculator application in Python using OOP principles.</p>",
        "due_at": "2024-03-15T23:59:00Z", "lock_at": "2024-03-16T23:59:00Z", "unlock_at": "2024-02-15T00:00:00Z",
        "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z",
        "points_possible": 200.0, "grading_type": "points", "submission_types": ["online_upload"],
        "has_submitted_submissions": True, "published": True, "only_visible_to_overrides": False,
        "assignment_group_id": 1, "position": 2, "peer_reviews": True, "automatic_peer_reviews": False,
        "grade_group_students_individually": False, "anonymous_submissions": False,
        "omit_from_final_grade": False, "moderated_grading": False, "rubric_id": 1,
        "html_url": "/courses/1/assignments/2", "needs_grading_count": 2,
    },
    3: {
        "id": 3, "course_id": 1, "name": "Final Exam", "description": "<p>Comprehensive final exam covering all course topics.</p>",
        "due_at": "2024-05-10T23:59:00Z", "lock_at": "2024-05-10T23:59:00Z", "unlock_at": "2024-05-10T08:00:00Z",
        "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z",
        "points_possible": 300.0, "grading_type": "points", "submission_types": ["online_quiz"],
        "has_submitted_submissions": False, "published": True, "only_visible_to_overrides": False,
        "assignment_group_id": 2, "position": 3, "peer_reviews": False, "automatic_peer_reviews": False,
        "grade_group_students_individually": False, "anonymous_submissions": True,
        "omit_from_final_grade": False, "moderated_grading": True, "rubric_id": None,
        "html_url": "/courses/1/assignments/3", "needs_grading_count": 0,
    },
    4: {
        "id": 4, "course_id": 2, "name": "Problem Set 1 - Limits", "description": "<p>Solve 10 limit problems using epsilon-delta definition.</p>",
        "due_at": "2024-02-05T23:59:00Z", "lock_at": None, "unlock_at": "2024-01-15T00:00:00Z",
        "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z",
        "points_possible": 50.0, "grading_type": "points", "submission_types": ["online_upload"],
        "has_submitted_submissions": True, "published": True, "only_visible_to_overrides": False,
        "assignment_group_id": 3, "position": 1, "peer_reviews": False, "automatic_peer_reviews": False,
        "grade_group_students_individually": False, "anonymous_submissions": False,
        "omit_from_final_grade": False, "moderated_grading": False, "rubric_id": None,
        "html_url": "/courses/2/assignments/4", "needs_grading_count": 2,
    },
    5: {
        "id": 5, "course_id": 3, "name": "Linked List Implementation", "description": "<p>Implement a doubly linked list in Python.</p>",
        "due_at": "2024-02-10T23:59:00Z", "lock_at": None, "unlock_at": "2024-01-20T00:00:00Z",
        "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z",
        "points_possible": 100.0, "grading_type": "points", "submission_types": ["online_upload"],
        "has_submitted_submissions": True, "published": True, "only_visible_to_overrides": False,
        "assignment_group_id": 4, "position": 1, "peer_reviews": False, "automatic_peer_reviews": False,
        "grade_group_students_individually": False, "anonymous_submissions": False,
        "omit_from_final_grade": False, "moderated_grading": False, "rubric_id": 2,
        "html_url": "/courses/3/assignments/5", "needs_grading_count": 0,
    },
}

# ─────────────────────────────────────────────
# ASSIGNMENT GROUPS
# ─────────────────────────────────────────────
ASSIGNMENT_GROUPS = {
    1: {"id": 1, "course_id": 1, "name": "Programming Assignments", "position": 1, "group_weight": 60.0, "rules": {}, "sis_source_id": None, "integration_data": {}},
    2: {"id": 2, "course_id": 1, "name": "Exams", "position": 2, "group_weight": 40.0, "rules": {}, "sis_source_id": None, "integration_data": {}},
    3: {"id": 3, "course_id": 2, "name": "Problem Sets", "position": 1, "group_weight": 50.0, "rules": {}, "sis_source_id": None, "integration_data": {}},
    4: {"id": 4, "course_id": 3, "name": "Lab Assignments", "position": 1, "group_weight": 70.0, "rules": {}, "sis_source_id": None, "integration_data": {}},
}

# ─────────────────────────────────────────────
# QUIZZES
# ─────────────────────────────────────────────
QUIZZES = {
    1: {
        "id": 1, "course_id": 1, "title": "Python Basics Quiz", "html_url": "/courses/1/quizzes/1",
        "mobile_url": "/courses/1/quizzes/1?persist_headless=1",
        "description": "<p>Test your understanding of Python basics: variables, data types, and operators.</p>",
        "quiz_type": "assignment", "time_limit": 30, "timer_autosubmit_disabled": False,
        "shuffle_answers": True, "show_correct_answers": True,
        "show_correct_answers_last_attempt": False, "show_correct_answers_at": None,
        "hide_correct_answers_at": None, "hide_results": None,
        "one_time_results": False, "scoring_policy": "keep_highest",
        "allowed_attempts": 2, "one_question_at_a_time": False,
        "question_count": 5, "points_possible": 50.0,
        "cant_go_back": False, "access_code": None, "ip_filter": None,
        "due_at": "2024-02-28T23:59:00Z", "lock_at": None, "unlock_at": "2024-01-20T00:00:00Z",
        "published": True, "unpublishable": False, "locked_for_user": False,
        "lock_info": None, "lock_explanation": None,
        "speedgrader_url": "/courses/1/gradebook/speed_grader?assignment_id=10",
        "quiz_extensions_url": "/courses/1/quizzes/1/extensions",
        "permissions": {"read": True, "submit": True, "create": True, "manage": True, "read_statistics": True, "review_grades": True, "update": True},
        "all_dates": [{"due_at": "2024-02-28T23:59:00Z", "unlock_at": "2024-01-20T00:00:00Z", "lock_at": None, "base": True}],
        "version_number": 3, "question_types": ["multiple_choice", "true_false"],
        "has_access_code": False, "assignment_id": 10,
        "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-15T00:00:00Z",
    },
    2: {
        "id": 2, "course_id": 1, "title": "OOP Concepts Quiz", "html_url": "/courses/1/quizzes/2",
        "mobile_url": "/courses/1/quizzes/2?persist_headless=1",
        "description": "<p>Object-Oriented Programming concepts: classes, inheritance, polymorphism.</p>",
        "quiz_type": "assignment", "time_limit": 45, "timer_autosubmit_disabled": False,
        "shuffle_answers": True, "show_correct_answers": False,
        "show_correct_answers_last_attempt": True, "show_correct_answers_at": None,
        "hide_correct_answers_at": None, "hide_results": "until_after_last_attempt",
        "one_time_results": False, "scoring_policy": "keep_latest",
        "allowed_attempts": 1, "one_question_at_a_time": True,
        "question_count": 10, "points_possible": 100.0,
        "cant_go_back": True, "access_code": None, "ip_filter": None,
        "due_at": "2024-04-01T23:59:00Z", "lock_at": "2024-04-02T00:00:00Z", "unlock_at": "2024-03-20T00:00:00Z",
        "published": True, "unpublishable": False, "locked_for_user": False,
        "lock_info": None, "lock_explanation": None,
        "speedgrader_url": "/courses/1/gradebook/speed_grader?assignment_id=11",
        "quiz_extensions_url": "/courses/1/quizzes/2/extensions",
        "permissions": {"read": True, "submit": True, "create": True, "manage": True, "read_statistics": True, "review_grades": True, "update": True},
        "all_dates": [{"due_at": "2024-04-01T23:59:00Z", "unlock_at": "2024-03-20T00:00:00Z", "lock_at": "2024-04-02T00:00:00Z", "base": True}],
        "version_number": 1, "question_types": ["multiple_choice", "short_answer", "multiple_answers"],
        "has_access_code": False, "assignment_id": 11,
        "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-02-01T00:00:00Z",
    },
    3: {
        "id": 3, "course_id": 2, "title": "Limits & Continuity Quiz", "html_url": "/courses/2/quizzes/3",
        "mobile_url": "/courses/2/quizzes/3?persist_headless=1",
        "description": "<p>Quiz on limits, continuity and the epsilon-delta definition.</p>",
        "quiz_type": "graded_survey", "time_limit": 60, "timer_autosubmit_disabled": False,
        "shuffle_answers": False, "show_correct_answers": True,
        "show_correct_answers_last_attempt": False, "show_correct_answers_at": None,
        "hide_correct_answers_at": None, "hide_results": None,
        "one_time_results": False, "scoring_policy": "keep_highest",
        "allowed_attempts": 3, "one_question_at_a_time": False,
        "question_count": 8, "points_possible": 80.0,
        "cant_go_back": False, "access_code": None, "ip_filter": None,
        "due_at": "2024-03-01T23:59:00Z", "lock_at": None, "unlock_at": "2024-02-15T00:00:00Z",
        "published": True, "unpublishable": False, "locked_for_user": False,
        "lock_info": None, "lock_explanation": None,
        "speedgrader_url": "/courses/2/gradebook/speed_grader?assignment_id=12",
        "quiz_extensions_url": "/courses/2/quizzes/3/extensions",
        "permissions": {"read": True, "submit": True, "create": True, "manage": True, "read_statistics": True, "review_grades": True, "update": True},
        "all_dates": [{"due_at": "2024-03-01T23:59:00Z", "unlock_at": "2024-02-15T00:00:00Z", "lock_at": None, "base": True}],
        "version_number": 2, "question_types": ["multiple_choice", "numerical"],
        "has_access_code": False, "assignment_id": 12,
        "created_at": "2024-01-12T00:00:00Z", "updated_at": "2024-01-20T00:00:00Z",
    },
}

# ─────────────────────────────────────────────
# QUIZ QUESTIONS
# ─────────────────────────────────────────────
QUIZ_QUESTIONS = {
    1: [
        {"id": 1, "quiz_id": 1, "position": 1, "question_name": "Q1", "question_type": "multiple_choice_question", "question_text": "What is the correct way to declare a variable in Python?", "points_possible": 10.0, "correct_comments": "Correct!", "incorrect_comments": "In Python, variables are declared by simply assigning a value.", "neutral_comments": "", "answers": [{"id": 1, "text": "int x = 5", "weight": 0}, {"id": 2, "text": "var x = 5", "weight": 0}, {"id": 3, "text": "x = 5", "weight": 100}, {"id": 4, "text": "declare x = 5", "weight": 0}]},
        {"id": 2, "quiz_id": 1, "position": 2, "question_name": "Q2", "question_type": "true_false_question", "question_text": "Python is a statically typed language.", "points_possible": 10.0, "correct_comments": "Correct!", "incorrect_comments": "Python is dynamically typed.", "neutral_comments": "", "answers": [{"id": 5, "text": "True", "weight": 0}, {"id": 6, "text": "False", "weight": 100}]},
        {"id": 3, "quiz_id": 1, "position": 3, "question_name": "Q3", "question_type": "multiple_choice_question", "question_text": "Which data type is used to store a sequence of characters?", "points_possible": 10.0, "correct_comments": "Correct!", "incorrect_comments": "Strings store sequences of characters.", "neutral_comments": "", "answers": [{"id": 7, "text": "int", "weight": 0}, {"id": 8, "text": "float", "weight": 0}, {"id": 9, "text": "str", "weight": 100}, {"id": 10, "text": "bool", "weight": 0}]},
        {"id": 4, "quiz_id": 1, "position": 4, "question_name": "Q4", "question_type": "multiple_choice_question", "question_text": "What does the `len()` function return?", "points_possible": 10.0, "correct_comments": "Correct!", "incorrect_comments": "len() returns the number of items in an object.", "neutral_comments": "", "answers": [{"id": 11, "text": "The last element", "weight": 0}, {"id": 12, "text": "The number of items", "weight": 100}, {"id": 13, "text": "The first element", "weight": 0}, {"id": 14, "text": "A sorted list", "weight": 0}]},
        {"id": 5, "quiz_id": 1, "position": 5, "question_name": "Q5", "question_type": "true_false_question", "question_text": "In Python, lists are mutable.", "points_possible": 10.0, "correct_comments": "Correct!", "incorrect_comments": "Lists are mutable, tuples are not.", "neutral_comments": "", "answers": [{"id": 15, "text": "True", "weight": 100}, {"id": 16, "text": "False", "weight": 0}]},
    ],
    2: [
        {"id": 6, "quiz_id": 2, "position": 1, "question_name": "Q1", "question_type": "multiple_choice_question", "question_text": "Which keyword is used to define a class in Python?", "points_possible": 10.0, "correct_comments": "Correct!", "incorrect_comments": "Use the `class` keyword.", "neutral_comments": "", "answers": [{"id": 17, "text": "def", "weight": 0}, {"id": 18, "text": "class", "weight": 100}, {"id": 19, "text": "object", "weight": 0}, {"id": 20, "text": "type", "weight": 0}]},
        {"id": 7, "quiz_id": 2, "position": 2, "question_name": "Q2", "question_type": "short_answer_question", "question_text": "What method is called when a new instance of a class is created?", "points_possible": 10.0, "correct_comments": "Correct!", "incorrect_comments": "__init__ is the constructor method.", "neutral_comments": "", "answers": [{"id": 21, "text": "__init__", "weight": 100}]},
    ],
}

# ─────────────────────────────────────────────
# QUIZ SUBMISSIONS
# ─────────────────────────────────────────────
QUIZ_SUBMISSIONS = {
    1: {
        "id": 1, "quiz_id": 1, "user_id": 3, "course_id": 1,
        "submission_id": 101, "started_at": "2024-02-28T20:00:00Z",
        "finished_at": "2024-02-28T20:25:00Z", "end_at": "2024-02-28T20:30:00Z",
        "attempt": 1, "extra_attempts": None, "extra_time": None,
        "time_spent": 1500, "score": 40.0, "score_before_regrade": None,
        "kept_score": 40.0, "fudge_points": None, "workflow_state": "complete",
        "quiz_points_possible": 50.0, "quiz_version": 3,
        "html_url": "/courses/1/quizzes/1/submissions/1",
    },
    2: {
        "id": 2, "quiz_id": 1, "user_id": 4, "course_id": 1,
        "submission_id": 102, "started_at": "2024-02-28T21:00:00Z",
        "finished_at": "2024-02-28T21:28:00Z", "end_at": "2024-02-28T21:30:00Z",
        "attempt": 1, "extra_attempts": None, "extra_time": None,
        "time_spent": 1680, "score": 30.0, "score_before_regrade": None,
        "kept_score": 30.0, "fudge_points": None, "workflow_state": "complete",
        "quiz_points_possible": 50.0, "quiz_version": 3,
        "html_url": "/courses/1/quizzes/1/submissions/2",
    },
    3: {
        "id": 3, "quiz_id": 1, "user_id": 5, "course_id": 1,
        "submission_id": 103, "started_at": "2024-02-27T18:00:00Z",
        "finished_at": "2024-02-27T18:22:00Z", "end_at": "2024-02-28T23:59:00Z",
        "attempt": 2, "extra_attempts": None, "extra_time": None,
        "time_spent": 1320, "score": 50.0, "score_before_regrade": 45.0,
        "kept_score": 50.0, "fudge_points": None, "workflow_state": "complete",
        "quiz_points_possible": 50.0, "quiz_version": 3,
        "html_url": "/courses/1/quizzes/1/submissions/3",
    },
}

# ─────────────────────────────────────────────
# QUIZ STATISTICS
# ─────────────────────────────────────────────
QUIZ_STATISTICS = {
    1: {
        "id": 1,
        "quiz_id": 1,
        "course_id": 1,
        "anonymous_survey": False,
        "speed_grader_url": "/courses/1/gradebook/speed_grader?assignment_id=10",
        "quiz_submissions_zip_url": "/courses/1/quizzes/1/submissions?zip=1",
        "points_possible": 50.0,
        "anonymous_survey": False,
        "multiple_attempts_exist": True,
        "generated_at": "2024-03-01T00:00:00Z",
        "includes_all_versions": False,
        "submission_statistics": {
            "score_average": 40.0,
            "score_high": 50.0,
            "score_low": 30.0,
            "score_stdev": 8.16,
            "correct_count_average": 4.0,
            "incorrect_count_average": 1.0,
            "duration_average": 1500.0,
            "unique_count": 3,
        },
        "question_statistics": [
            {
                "id": 1, "question_type": "multiple_choice_question",
                "question_text": "What is the correct way to declare a variable in Python?",
                "position": 1, "responses": 3, "correct": 3,
                "point_biserial": 0.82,
                "answers": [
                    {"id": 1, "text": "int x = 5", "correct": False, "responses": 0, "user_ids": [], "user_names": []},
                    {"id": 2, "text": "var x = 5", "correct": False, "responses": 0, "user_ids": [], "user_names": []},
                    {"id": 3, "text": "x = 5", "correct": True, "responses": 3, "user_ids": [3, 4, 5], "user_names": ["Carol White", "David Lee", "Eva Chen"]},
                    {"id": 4, "text": "declare x = 5", "correct": False, "responses": 0, "user_ids": [], "user_names": []},
                ],
            },
            {
                "id": 2, "question_type": "true_false_question",
                "question_text": "Python is a statically typed language.",
                "position": 2, "responses": 3, "correct": 2,
                "point_biserial": 0.55,
                "answers": [
                    {"id": 5, "text": "True", "correct": False, "responses": 1, "user_ids": [4], "user_names": ["David Lee"]},
                    {"id": 6, "text": "False", "correct": True, "responses": 2, "user_ids": [3, 5], "user_names": ["Carol White", "Eva Chen"]},
                ],
            },
        ],
    }
}

# ─────────────────────────────────────────────
# RUBRICS
# ─────────────────────────────────────────────
RUBRICS = {
    1: {
        "id": 1,
        "title": "Midterm Project Rubric",
        "context_id": 1,
        "context_type": "Course",
        "points_possible": 200.0,
        "reusable": True,
        "public": False,
        "read_only": False,
        "free_form_criterion_comments": False,
        "hide_score_total": False,
        "data": [
            {
                "id": "crit_1", "description": "Code Quality",
                "long_description": "Is the code clean, readable, and well-organized?",
                "points": 50.0, "criterion_use_range": False,
                "ratings": [
                    {"id": "rating_1a", "description": "Excellent", "long_description": "Code is clean, well-commented, and follows PEP8.", "points": 50.0},
                    {"id": "rating_1b", "description": "Satisfactory", "long_description": "Code is mostly clean with minor issues.", "points": 35.0},
                    {"id": "rating_1c", "description": "Needs Improvement", "long_description": "Code has significant quality issues.", "points": 20.0},
                    {"id": "rating_1d", "description": "Unsatisfactory", "long_description": "Code is unreadable or non-functional.", "points": 0.0},
                ],
            },
            {
                "id": "crit_2", "description": "Functionality",
                "long_description": "Does the program work correctly for all test cases?",
                "points": 80.0, "criterion_use_range": False,
                "ratings": [
                    {"id": "rating_2a", "description": "All tests pass", "long_description": "Program works correctly for all provided test cases.", "points": 80.0},
                    {"id": "rating_2b", "description": "Most tests pass", "long_description": "Program works correctly for 75%+ of test cases.", "points": 60.0},
                    {"id": "rating_2c", "description": "Some tests pass", "long_description": "Program works correctly for 50%+ of test cases.", "points": 40.0},
                    {"id": "rating_2d", "description": "Few tests pass", "long_description": "Program works for less than 50% of test cases.", "points": 10.0},
                ],
            },
            {
                "id": "crit_3", "description": "OOP Design",
                "long_description": "Does the solution properly use Object-Oriented principles?",
                "points": 50.0, "criterion_use_range": False,
                "ratings": [
                    {"id": "rating_3a", "description": "Excellent OOP", "long_description": "Proper use of classes, inheritance, and encapsulation.", "points": 50.0},
                    {"id": "rating_3b", "description": "Good OOP", "long_description": "Classes used correctly but missing some OOP patterns.", "points": 35.0},
                    {"id": "rating_3c", "description": "Basic OOP", "long_description": "Classes defined but not used effectively.", "points": 20.0},
                    {"id": "rating_3d", "description": "No OOP", "long_description": "Solution does not use OOP.", "points": 0.0},
                ],
            },
            {
                "id": "crit_4", "description": "Documentation",
                "long_description": "Is the code properly documented with docstrings and comments?",
                "points": 20.0, "criterion_use_range": False,
                "ratings": [
                    {"id": "rating_4a", "description": "Well Documented", "long_description": "All functions and classes have docstrings.", "points": 20.0},
                    {"id": "rating_4b", "description": "Partially Documented", "long_description": "Some documentation present.", "points": 10.0},
                    {"id": "rating_4c", "description": "Minimal Documentation", "long_description": "Little to no documentation.", "points": 5.0},
                    {"id": "rating_4d", "description": "No Documentation", "long_description": "No documentation present.", "points": 0.0},
                ],
            },
        ],
        "assessments": None,
        "associations": [{"id": 1, "association_id": 2, "association_type": "Assignment", "use_for_grading": True, "summary_data": {}, "purpose": "grading", "hide_score_total": False, "hide_points": False, "hide_outcome_results": False}],
        "created_at": "2024-01-10T00:00:00Z",
        "updated_at": "2024-01-10T00:00:00Z",
    },
    2: {
        "id": 2,
        "title": "Linked List Implementation Rubric",
        "context_id": 3,
        "context_type": "Course",
        "points_possible": 100.0,
        "reusable": True,
        "public": False,
        "read_only": False,
        "free_form_criterion_comments": False,
        "hide_score_total": False,
        "data": [
            {
                "id": "crit_5", "description": "Correctness",
                "long_description": "All operations (insert, delete, traverse) work correctly.",
                "points": 60.0, "criterion_use_range": False,
                "ratings": [
                    {"id": "rating_5a", "description": "Fully Correct", "long_description": "All operations work with edge cases handled.", "points": 60.0},
                    {"id": "rating_5b", "description": "Mostly Correct", "long_description": "Most operations work; minor bugs.", "points": 45.0},
                    {"id": "rating_5c", "description": "Partially Correct", "long_description": "Some operations work.", "points": 25.0},
                    {"id": "rating_5d", "description": "Incorrect", "long_description": "Implementation does not work.", "points": 0.0},
                ],
            },
            {
                "id": "crit_6", "description": "Time Complexity",
                "long_description": "Operations meet expected Big-O requirements.",
                "points": 40.0, "criterion_use_range": False,
                "ratings": [
                    {"id": "rating_6a", "description": "Optimal", "long_description": "All operations meet expected complexity.", "points": 40.0},
                    {"id": "rating_6b", "description": "Acceptable", "long_description": "Most operations meet expected complexity.", "points": 25.0},
                    {"id": "rating_6c", "description": "Suboptimal", "long_description": "Operations are correct but not efficient.", "points": 10.0},
                    {"id": "rating_6d", "description": "No consideration", "long_description": "No attention to complexity.", "points": 0.0},
                ],
            },
        ],
        "assessments": None,
        "associations": [{"id": 2, "association_id": 5, "association_type": "Assignment", "use_for_grading": True, "summary_data": {}, "purpose": "grading", "hide_score_total": False, "hide_points": False, "hide_outcome_results": False}],
        "created_at": "2024-01-12T00:00:00Z",
        "updated_at": "2024-01-12T00:00:00Z",
    },
}

# ─────────────────────────────────────────────
# RUBRIC ASSESSMENTS
# ─────────────────────────────────────────────
RUBRIC_ASSESSMENTS = {
    1: {
        "id": 1, "rubric_id": 1, "rubric_association_id": 1,
        "score": 165.0, "artifact_type": "Submission",
        "artifact_id": 201, "artifact_attempt": 1,
        "assessor_id": 1, "user_id": 3,
        "data": [
            {"criterion_id": "crit_1", "points": 35.0, "comments": "Good structure, minor PEP8 issues.", "rating_id": "rating_1b"},
            {"criterion_id": "crit_2", "points": 80.0, "comments": "All test cases pass!", "rating_id": "rating_2a"},
            {"criterion_id": "crit_3", "points": 35.0, "comments": "Good use of classes, could add more abstraction.", "rating_id": "rating_3b"},
            {"criterion_id": "crit_4", "points": 15.0, "comments": "Most functions documented.", "rating_id": "rating_4b"},
        ],
        "created_at": "2024-03-20T00:00:00Z",
        "updated_at": "2024-03-20T00:00:00Z",
    }
}

# ─────────────────────────────────────────────
# PAGES (Wiki Pages)
# ─────────────────────────────────────────────
PAGES = {
    1: {
        "page_id": 1, "url": "course-syllabus", "title": "Course Syllabus",
        "course_id": 1,
        "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-12T00:00:00Z",
        "hide_from_students": False, "editing_roles": "teachers",
        "last_edited_by": {"id": 1, "display_name": "Alice Johnson", "avatar_image_url": "https://i.pravatar.cc/150?u=alice", "html_url": "/users/1"},
        "body": "<h1>CS101 - Introduction to Python</h1><h2>Course Overview</h2><p>This course introduces the fundamental concepts of programming using Python...</p><h2>Grading Policy</h2><ul><li>Assignments: 60%</li><li>Final Exam: 40%</li></ul>",
        "published": True, "front_page": True,
        "locked_for_user": False, "lock_info": None, "lock_explanation": None,
    },
    2: {
        "page_id": 2, "url": "week-1-introduction", "title": "Week 1 - Introduction to Python",
        "course_id": 1,
        "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-14T00:00:00Z",
        "hide_from_students": False, "editing_roles": "teachers",
        "last_edited_by": {"id": 1, "display_name": "Alice Johnson", "avatar_image_url": "https://i.pravatar.cc/150?u=alice", "html_url": "/users/1"},
        "body": "<h2>Week 1 Topics</h2><ul><li>What is Python?</li><li>Installing Python and setting up your environment</li><li>Variables and Data Types</li><li>Basic I/O with print() and input()</li></ul><h3>Resources</h3><p>Read chapters 1-2 of the textbook.</p>",
        "published": True, "front_page": False,
        "locked_for_user": False, "lock_info": None, "lock_explanation": None,
    },
    3: {
        "page_id": 3, "url": "week-2-control-flow", "title": "Week 2 - Control Flow",
        "course_id": 1,
        "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-21T00:00:00Z",
        "hide_from_students": False, "editing_roles": "teachers",
        "last_edited_by": {"id": 1, "display_name": "Alice Johnson", "avatar_image_url": "https://i.pravatar.cc/150?u=alice", "html_url": "/users/1"},
        "body": "<h2>Week 2 Topics</h2><ul><li>if/elif/else statements</li><li>for and while loops</li><li>break, continue, and pass</li><li>List comprehensions</li></ul>",
        "published": True, "front_page": False,
        "locked_for_user": False, "lock_info": None, "lock_explanation": None,
    },
    4: {
        "page_id": 4, "url": "calculus-resources", "title": "Calculus Reference Resources",
        "course_id": 2,
        "created_at": "2024-01-12T00:00:00Z", "updated_at": "2024-01-12T00:00:00Z",
        "hide_from_students": False, "editing_roles": "teachers",
        "last_edited_by": {"id": 2, "display_name": "Bob Martinez", "avatar_image_url": "https://i.pravatar.cc/150?u=bob", "html_url": "/users/2"},
        "body": "<h1>Useful Calculus Resources</h1><ul><li><a href='https://www.khanacademy.org/math/calculus-1'>Khan Academy - Calculus 1</a></li><li>Textbook: Stewart Calculus 8th Edition</li></ul>",
        "published": True, "front_page": True,
        "locked_for_user": False, "lock_info": None, "lock_explanation": None,
    },
    5: {
        "page_id": 5, "url": "hidden-draft-page", "title": "Draft: Upcoming Topics (Hidden)",
        "course_id": 1,
        "created_at": "2024-01-10T00:00:00Z", "updated_at": "2024-01-10T00:00:00Z",
        "hide_from_students": True, "editing_roles": "teachers",
        "last_edited_by": {"id": 1, "display_name": "Alice Johnson", "avatar_image_url": "https://i.pravatar.cc/150?u=alice", "html_url": "/users/1"},
        "body": "<p>Topics for the second half of the semester (draft, not finalized).</p>",
        "published": False, "front_page": False,
        "locked_for_user": True, "lock_info": {"missing_permission": "read"}, "lock_explanation": "This page is currently unavailable.",
    },
}

# ─────────────────────────────────────────────
# MODULES
# ─────────────────────────────────────────────
MODULES = {
    1: {
        "id": 1, "course_id": 1, "name": "Module 1: Python Fundamentals",
        "position": 1, "unlock_at": None, "require_sequential_progress": True,
        "prerequisite_module_ids": [], "items_count": 4,
        "items_url": "/api/v1/courses/1/modules/1/items",
        "published": True, "workflow_state": "active",
        "state": "completed", "completed_at": None,
        "publish_final_grade": False,
    },
    2: {
        "id": 2, "course_id": 1, "name": "Module 2: Object-Oriented Python",
        "position": 2, "unlock_at": None, "require_sequential_progress": True,
        "prerequisite_module_ids": [1], "items_count": 3,
        "items_url": "/api/v1/courses/1/modules/2/items",
        "published": True, "workflow_state": "active",
        "state": "unlocked", "completed_at": None,
        "publish_final_grade": False,
    },
    3: {
        "id": 3, "course_id": 1, "name": "Module 3: Final Project",
        "position": 3, "unlock_at": "2024-04-01T00:00:00Z", "require_sequential_progress": True,
        "prerequisite_module_ids": [1, 2], "items_count": 2,
        "items_url": "/api/v1/courses/1/modules/3/items",
        "published": True, "workflow_state": "active",
        "state": "locked", "completed_at": None,
        "publish_final_grade": True,
    },
}

MODULE_ITEMS = {
    1: [
        {"id": 1, "module_id": 1, "position": 1, "title": "Course Syllabus", "indent": 0, "type": "Page", "content_id": 1, "url": "/api/v1/courses/1/pages/course-syllabus", "html_url": "/courses/1/pages/course-syllabus", "published": True, "completion_requirement": {"type": "must_view"}},
        {"id": 2, "module_id": 1, "position": 2, "title": "Week 1 - Introduction to Python", "indent": 0, "type": "Page", "content_id": 2, "url": "/api/v1/courses/1/pages/week-1-introduction", "html_url": "/courses/1/pages/week-1-introduction", "published": True, "completion_requirement": {"type": "must_view"}},
        {"id": 3, "module_id": 1, "position": 3, "title": "Python Basics Quiz", "indent": 0, "type": "Quiz", "content_id": 1, "url": "/api/v1/courses/1/quizzes/1", "html_url": "/courses/1/quizzes/1", "published": True, "completion_requirement": {"type": "must_submit", "min_score": 30, "completed": False}},
        {"id": 4, "module_id": 1, "position": 4, "title": "Hello World Program", "indent": 0, "type": "Assignment", "content_id": 1, "url": "/api/v1/courses/1/assignments/1", "html_url": "/courses/1/assignments/1", "published": True, "completion_requirement": {"type": "must_submit", "completed": False}},
    ],
    2: [
        {"id": 5, "module_id": 2, "position": 1, "title": "Week 2 - Control Flow", "indent": 0, "type": "Page", "content_id": 3, "url": "/api/v1/courses/1/pages/week-2-control-flow", "html_url": "/courses/1/pages/week-2-control-flow", "published": True, "completion_requirement": {"type": "must_view"}},
        {"id": 6, "module_id": 2, "position": 2, "title": "OOP Concepts Quiz", "indent": 0, "type": "Quiz", "content_id": 2, "url": "/api/v1/courses/1/quizzes/2", "html_url": "/courses/1/quizzes/2", "published": True, "completion_requirement": {"type": "must_submit", "min_score": 60, "completed": False}},
        {"id": 7, "module_id": 2, "position": 3, "title": "Midterm Project - Calculator App", "indent": 0, "type": "Assignment", "content_id": 2, "url": "/api/v1/courses/1/assignments/2", "html_url": "/courses/1/assignments/2", "published": True, "completion_requirement": {"type": "must_submit", "completed": False}},
    ],
    3: [
        {"id": 8, "module_id": 3, "position": 1, "title": "Final Exam", "indent": 0, "type": "Assignment", "content_id": 3, "url": "/api/v1/courses/1/assignments/3", "html_url": "/courses/1/assignments/3", "published": True, "completion_requirement": {"type": "must_submit", "completed": False}},
        {"id": 9, "module_id": 3, "position": 2, "title": "External Resource - Python Docs", "indent": 1, "type": "ExternalUrl", "content_id": None, "external_url": "https://docs.python.org/3/", "html_url": "/courses/1/modules/items/9", "published": True, "completion_requirement": {"type": "must_view"}},
    ],
}

# ─────────────────────────────────────────────
# SUBMISSIONS
# ─────────────────────────────────────────────
SUBMISSIONS = {
    (1, 3): {"id": 201, "assignment_id": 1, "user_id": 3, "course_id": 1, "submitted_at": "2024-01-31T22:00:00Z", "graded_at": "2024-02-05T10:00:00Z", "grader_id": 1, "score": 92.0, "grade": "92", "workflow_state": "graded", "submission_type": "online_text_entry", "body": "print('Hello World')\nprint('I am Carol')", "late": False, "missing": False, "attempt": 1, "late_policy_status": None, "points_deducted": None, "grade_matches_current_submission": True, "attachments": [], "comments": []},
    (1, 4): {"id": 202, "assignment_id": 1, "user_id": 4, "course_id": 1, "submitted_at": "2024-02-01T20:00:00Z", "graded_at": None, "grader_id": None, "score": None, "grade": None, "workflow_state": "submitted", "submission_type": "online_text_entry", "body": "print('Hello World!')", "late": False, "missing": False, "attempt": 1, "late_policy_status": None, "points_deducted": None, "grade_matches_current_submission": True, "attachments": [], "comments": []},
    (2, 3): {"id": 203, "assignment_id": 2, "user_id": 3, "course_id": 1, "submitted_at": "2024-03-14T23:45:00Z", "graded_at": "2024-03-20T14:00:00Z", "grader_id": 1, "score": 165.0, "grade": "165", "workflow_state": "graded", "submission_type": "online_upload", "body": None, "late": False, "missing": False, "attempt": 1, "late_policy_status": None, "points_deducted": None, "grade_matches_current_submission": True, "attachments": [{"id": 1, "display_name": "calculator.py", "filename": "calculator.py", "content_type": "text/x-python", "size": 4500}], "comments": [{"id": 1, "comment": "Great work! Clean code structure.", "author": {"id": 1, "display_name": "Alice Johnson"}, "created_at": "2024-03-20T14:05:00Z"}]},
    (5, 4): {"id": 204, "assignment_id": 5, "user_id": 4, "course_id": 3, "submitted_at": "2024-02-09T18:00:00Z", "graded_at": "2024-02-12T10:00:00Z", "grader_id": 1, "score": 90.0, "grade": "90", "workflow_state": "graded", "submission_type": "online_upload", "body": None, "late": False, "missing": False, "attempt": 1, "late_policy_status": None, "points_deducted": None, "grade_matches_current_submission": True, "attachments": [{"id": 2, "display_name": "linked_list.py", "filename": "linked_list.py", "content_type": "text/x-python", "size": 3200}], "comments": []},
    (5, 5): {"id": 205, "assignment_id": 5, "user_id": 5, "course_id": 3, "submitted_at": "2024-02-08T21:00:00Z", "graded_at": "2024-02-12T11:00:00Z", "grader_id": 1, "score": 98.0, "grade": "98", "workflow_state": "graded", "submission_type": "online_upload", "body": None, "late": False, "missing": False, "attempt": 1, "late_policy_status": None, "points_deducted": None, "grade_matches_current_submission": True, "attachments": [{"id": 3, "display_name": "linked_list.py", "filename": "linked_list.py", "content_type": "text/x-python", "size": 5100}], "comments": [{"id": 2, "comment": "Excellent edge case handling!", "author": {"id": 1, "display_name": "Alice Johnson"}, "created_at": "2024-02-12T11:10:00Z"}]},
}

# ─────────────────────────────────────────────
# ANNOUNCEMENTS
# ─────────────────────────────────────────────
ANNOUNCEMENTS = {
    1: {
        "id": 1, "course_id": 1, "title": "Welcome to CS101!",
        "message": "<p>Welcome to Introduction to Python! Please review the syllabus and complete the Week 1 readings before our first class.</p>",
        "author": {"id": 1, "display_name": "Alice Johnson", "avatar_image_url": "https://i.pravatar.cc/150?u=alice"},
        "posted_at": "2024-01-14T08:00:00Z", "delayed_post_at": None,
        "discussion_type": "side_comment", "pinned": True, "locked": False,
        "position": 1, "subscribed": True,
        "read_state": "read", "unread_count": 0,
        "published": True, "allow_rating": False, "only_graders_can_rate": False,
        "sort_by_rating": False, "html_url": "/courses/1/discussion_topics/1",
    },
    2: {
        "id": 2, "course_id": 1, "title": "Midterm Project Details Posted",
        "message": "<p>The details for the midterm project have been posted. Please check Assignment 2 for full requirements. Office hours this week: Tue/Thu 2-4pm.</p>",
        "author": {"id": 1, "display_name": "Alice Johnson", "avatar_image_url": "https://i.pravatar.cc/150?u=alice"},
        "posted_at": "2024-02-15T10:00:00Z", "delayed_post_at": None,
        "discussion_type": "side_comment", "pinned": False, "locked": False,
        "position": 2, "subscribed": True,
        "read_state": "unread", "unread_count": 3,
        "published": True, "allow_rating": False, "only_graders_can_rate": False,
        "sort_by_rating": False, "html_url": "/courses/1/discussion_topics/2",
    },
}

# ─────────────────────────────────────────────
# DISCUSSION TOPICS
# ─────────────────────────────────────────────
DISCUSSION_TOPICS = {
    1: {
        "id": 10, "course_id": 1, "title": "Introduce Yourself!",
        "message": "<p>Tell us a bit about yourself, your programming background, and why you're taking this course.</p>",
        "author": {"id": 1, "display_name": "Alice Johnson"},
        "posted_at": "2024-01-15T09:00:00Z", "last_reply_at": "2024-01-20T14:00:00Z",
        "discussion_type": "threaded", "pinned": True, "locked": False,
        "position": 1, "published": True, "subscribed": True,
        "assignment_id": None, "delayed_post_at": None, "lock_at": None,
        "podcast_enabled": False, "podcast_has_student_posts": False,
        "require_initial_post": True, "user_can_see_posts": True,
        "discussion_subentry_count": 3, "unread_count": 0, "read_state": "read",
        "html_url": "/courses/1/discussion_topics/10",
    },
    2: {
        "id": 11, "course_id": 1, "title": "Week 2 Discussion: Loops and Iteration",
        "message": "<p>Share an example from real life that could be modeled with a loop. How would you implement it in Python?</p>",
        "author": {"id": 1, "display_name": "Alice Johnson"},
        "posted_at": "2024-01-22T09:00:00Z", "last_reply_at": "2024-01-28T18:00:00Z",
        "discussion_type": "threaded", "pinned": False, "locked": False,
        "position": 2, "published": True, "subscribed": True,
        "assignment_id": None, "delayed_post_at": None, "lock_at": None,
        "podcast_enabled": False, "podcast_has_student_posts": False,
        "require_initial_post": True, "user_can_see_posts": True,
        "discussion_subentry_count": 5, "unread_count": 2, "read_state": "unread",
        "html_url": "/courses/1/discussion_topics/11",
    },
}

# Counters for auto-increment IDs
_id_counters = {
    "user": max(USERS.keys()) + 1,
    "course": max(COURSES.keys()) + 1,
    "quiz": max(QUIZZES.keys()) + 1,
    "rubric": max(RUBRICS.keys()) + 1,
    "page": max(PAGES.keys()) + 1,
    "assignment": max(ASSIGNMENTS.keys()) + 1,
    "enrollment": max(ENROLLMENTS.keys()) + 1,
    "module": max(MODULES.keys()) + 1,
    "announcement": max(ANNOUNCEMENTS.keys()) + 1,
    "discussion": max(DISCUSSION_TOPICS.keys()) + 1,
}

def next_id(resource: str) -> int:
    _id_counters[resource] = _id_counters.get(resource, 1)
    val = _id_counters[resource]
    _id_counters[resource] += 1
    return val
