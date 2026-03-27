from fastapi import APIRouter
from core.mock_db import MOCK_FILES

router = APIRouter(
    tags=["Files"],
)

# GET QUOTA INFORMATION

@router.get("/api/v1/courses/{course_id}/files/quota")
async def get_course_quota():
    return { "quota": 524288000, "quota_used": 402653184 }

@router.get("/api/v1/groups/{group_id}/files/quota")
async def get_group_quota():
    return { "quota": 524288000, "quota_used": 402653184 }

@router.get("/api/v1/users/{user_id}/files/quota")
async def get_user_quota():
    return { "quota": 524288000, "quota_used": 402653184 }

# LIST FILES

@router.get("/api/v1/courses/{course_id}/files")
async def list_course_files():
    return MOCK_FILES

@router.get("/api/v1/users/{user_id}/files")
async def list_user_files():
    return MOCK_FILES

@router.get("/api/v1/groups/{group_id}/files")
async def list_group_files():
    return MOCK_FILES

@router.get("/api/v1/folders/{id}/files")
async def list_folder_files():
    return MOCK_FILES

# Get public inline preview url

@router.get("/api/v1/files/{id}/public_url")
async def preview_url():
    return { "public_url": "https://example-bucket.s3.amazonaws.com/example-namespace/attachments/1/example-filename?AWSAccessKeyId=example-key&Expires=1400000000&Signature=example-signature" }