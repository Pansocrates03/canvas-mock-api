"""
Canvas Mock API - Auth / Security Utilities
"""
from fastapi import HTTPException, Header, Depends
from typing import Optional
from data.mock_data import OAUTH_TOKENS, USERS


def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Validate Bearer token from Authorization header and return the user dict.
    Accepts: Authorization: Bearer <token>
    Also accepts a loose token without 'Bearer' prefix for convenience.
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail={"status": "unauthenticated", "errors": [{"message": "Invalid access token."}]},
            headers={"WWW-Authenticate": "Bearer realm=\"application\""},
        )

    token = authorization
    if authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()

    token_data = OAUTH_TOKENS.get(token)
    if not token_data:
        raise HTTPException(
            status_code=401,
            detail={"status": "unauthenticated", "errors": [{"message": "Invalid access token."}]},
            headers={"WWW-Authenticate": "Bearer realm=\"application\""},
        )

    user = USERS.get(token_data["user_id"])
    if not user:
        raise HTTPException(status_code=401, detail={"errors": [{"message": "User not found."}]})

    return user


def require_teacher(current_user=Depends(get_current_user)):
    """Require the authenticated user to have a teacher role."""
    if "teacher" not in current_user.get("roles", []):
        raise HTTPException(
            status_code=403,
            detail={"status": "unauthorized", "errors": [{"message": "user not authorized to perform that action"}]},
        )
    return current_user


def optional_auth(authorization: Optional[str] = Header(None)):
    """Return the current user if authenticated, None otherwise."""
    if not authorization:
        return None
    try:
        return get_current_user(authorization)
    except HTTPException:
        return None
