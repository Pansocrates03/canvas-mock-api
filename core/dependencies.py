from fastapi import Header, HTTPException
from typing import Optional

def verify_token(authorization: Optional[str] = Header(None)):
    """Simula la validación del Bearer token de Canvas."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="user authorization required")
    return authorization.split(" ")[1]