from pydantic import BaseModel

class GrantTokenModel(BaseModel):
    access_token: str
    token_type: str
    user: dict[int, str]
    refresh_token: str
    expires_in: int
    canvas_region: str

class SessionToken(BaseModel):
    session_url: str