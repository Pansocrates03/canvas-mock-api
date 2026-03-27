from fastapi import APIRouter
from modules.oauth.schemas import GrantTokenModel, SessionToken

router = APIRouter(
    tags=["Oauth"],
)

#@router.get("/login/oauth2/auth")
#async def acces_token_request():
#    return "lol"

@router.post("/login/oauth2/token", response_model=GrantTokenModel)
async def acces_token_request():
    return {
        "access_token": "1/fFAGRNJru1FTz70BzhT3Zg",
        "token_type": "Bearer",
        "user": {"id":42, "name": "Jimi Hendrix"},
        "refresh_token": "tIh2YBWGiC0GgGRglT9Ylwv2MnTvy8csfGyfK2PqZmkFYYqYZ0wui4tzI7uBwnN2",
        "expires_in": 3600,
        "canvas_region": "us-east-1"
    }

@router.get("/login/session_token", response_model=SessionToken)
async def request_session_url():
    return   {
        "session_url": "https://canvas.instructure.com/opaque_url"
    }
  