"""
Canvas Mock API – OAuth 2.0 Endpoints
Implements: https://canvas.instructure.com/doc/api/file.oauth_endpoints.html
"""
import uuid
import secrets
from fastapi import APIRouter, HTTPException, Form, Query, Request
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Optional
from data.mock_data import OAUTH_TOKENS, OAUTH_CODES, REFRESH_TOKENS, USERS

router = APIRouter(tags=["OAuth"])

# ─── Mock registered developer keys / apps ───────────────────────────────────
REGISTERED_APPS = {
    "mock_client_id_001": {
        "client_secret": "mock_client_secret_001",
        "redirect_uris": ["https://localhost/callback", "http://localhost:8080/callback", "urn:ietf:wg:oauth:2.0:oob"],
        "name": "Mock Developer Application",
    }
}


@router.get(
    "/login/oauth2/auth",
    summary="OAuth2 – Authorization endpoint",
    description=(
        "Redirects the user to the Canvas login page, then to the redirect_uri "
        "with an authorization code. For testing, use `?state=test&mock_user_id=1` "
        "to simulate a login as a specific user."
    ),
)
async def oauth_authorize(
    client_id: str = Query(..., description="The client_id of your developer key"),
    redirect_uri: str = Query(..., description="The callback URI"),
    response_type: str = Query(..., description="Must be 'code'"),
    state: Optional[str] = Query(None, description="Opaque state value"),
    scope: Optional[str] = Query(None, description="Space-separated scopes"),
    mock_user_id: Optional[int] = Query(1, description="Simulate login as this user ID (mock only)"),
):
    if response_type != "code":
        raise HTTPException(status_code=400, detail={"error": "unsupported_response_type", "error_description": "Only 'code' is supported."})

    app = REGISTERED_APPS.get(client_id)
    if not app:
        raise HTTPException(status_code=400, detail={"error": "invalid_client", "error_description": "Unknown client_id."})

    if redirect_uri not in app["redirect_uris"]:
        raise HTTPException(status_code=400, detail={"error": "invalid_redirect_uri", "error_description": "Redirect URI not registered."})

    user = USERS.get(mock_user_id)
    if not user:
        raise HTTPException(status_code=400, detail={"error": "invalid_user", "error_description": f"Mock user {mock_user_id} not found."})

    code = secrets.token_urlsafe(32)
    OAUTH_CODES[code] = {"user_id": mock_user_id, "scope": scope or "*", "client_id": client_id}

    if redirect_uri == "urn:ietf:wg:oauth:2.0:oob":
        return {
            "message": "Authorization successful (OOB flow). Use this code in the token exchange.",
            "code": code,
            "state": state,
        }

    sep = "&" if "?" in redirect_uri else "?"
    location = f"{redirect_uri}{sep}code={code}"
    if state:
        location += f"&state={state}"
    return RedirectResponse(url=location, status_code=302)


@router.post(
    "/login/oauth2/token",
    summary="OAuth2 – Token endpoint",
    description=(
        "Exchange an authorization code or refresh token for an access token. "
        "Also supports client_credentials grant type."
    ),
)
async def oauth_token(
    grant_type: str = Form(..., description="'authorization_code', 'refresh_token', or 'client_credentials'"),
    client_id: Optional[str] = Form(None),
    client_secret: Optional[str] = Form(None),
    redirect_uri: Optional[str] = Form(None),
    code: Optional[str] = Form(None, description="Required for authorization_code grant"),
    refresh_token: Optional[str] = Form(None, description="Required for refresh_token grant"),
    replace_tokens: Optional[bool] = Form(False),
):
    # Validate client
    if client_id and client_secret:
        app = REGISTERED_APPS.get(client_id)
        if not app or app["client_secret"] != client_secret:
            raise HTTPException(status_code=401, detail={"error": "invalid_client", "error_description": "Invalid client credentials."})

    if grant_type == "authorization_code":
        if not code:
            raise HTTPException(status_code=400, detail={"error": "invalid_request", "error_description": "Code is required."})
        code_data = OAUTH_CODES.pop(code, None)
        if not code_data:
            raise HTTPException(status_code=400, detail={"error": "invalid_grant", "error_description": "Authorization code not found or already used."})

        user_id = code_data["user_id"]
        user = USERS[user_id]
        access_token = f"access_{secrets.token_urlsafe(24)}"
        refresh_tok = f"refresh_{secrets.token_urlsafe(24)}"

        OAUTH_TOKENS[access_token] = {"user_id": user_id, "scope": code_data.get("scope", "*"), "expires_in": 3600, "token_type": "Bearer"}
        REFRESH_TOKENS[refresh_tok] = {"user_id": user_id, "access_token": access_token}

        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": refresh_tok,
            "scope": code_data.get("scope", "*"),
            "user": {"id": user_id, "name": user["name"], "global_id": str(user_id)},
            "canvas_region": "us-east-1",
        }

    elif grant_type == "refresh_token":
        if not refresh_token:
            raise HTTPException(status_code=400, detail={"error": "invalid_request", "error_description": "refresh_token is required."})
        rdata = REFRESH_TOKENS.get(refresh_token)
        if not rdata:
            raise HTTPException(status_code=400, detail={"error": "invalid_grant", "error_description": "Invalid refresh token."})

        user_id = rdata["user_id"]
        user = USERS[user_id]
        new_access = f"access_{secrets.token_urlsafe(24)}"
        OAUTH_TOKENS[new_access] = {"user_id": user_id, "scope": "*", "expires_in": 3600, "token_type": "Bearer"}
        rdata["access_token"] = new_access

        return {
            "access_token": new_access,
            "token_type": "Bearer",
            "expires_in": 3600,
            "user": {"id": user_id, "name": user["name"], "global_id": str(user_id)},
        }

    elif grant_type == "client_credentials":
        if not client_id or not client_secret:
            raise HTTPException(status_code=400, detail={"error": "invalid_request", "error_description": "client_id and client_secret are required."})
        access_token = f"cc_{secrets.token_urlsafe(24)}"
        OAUTH_TOKENS[access_token] = {"user_id": 1, "scope": "*", "expires_in": 3600, "token_type": "Bearer"}
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "*",
        }

    else:
        raise HTTPException(status_code=400, detail={"error": "unsupported_grant_type", "error_description": f"Unsupported grant_type: {grant_type}"})


@router.delete(
    "/login/oauth2/token",
    summary="OAuth2 – Revoke token",
    description="Revoke an access token.",
)
async def oauth_revoke_token(
    access_token: Optional[str] = Form(None),
    authorization: Optional[str] = None,
):
    token = access_token
    if not token and authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()

    if token and token in OAUTH_TOKENS:
        del OAUTH_TOKENS[token]
        return {"message": "Token revoked successfully."}
    raise HTTPException(status_code=400, detail={"error": "invalid_token", "error_description": "Token not found or already revoked."})


@router.get(
    "/login/oauth2/token_info",
    summary="OAuth2 – Token introspection (mock extension)",
    description="Inspect the currently active access token.",
)
async def token_info(authorization: Optional[str] = None):
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    if not token or token not in OAUTH_TOKENS:
        raise HTTPException(status_code=401, detail={"error": "invalid_token"})
    data = OAUTH_TOKENS[token]
    user = USERS.get(data["user_id"], {})
    return {
        "token_type": "Bearer",
        "user_id": data["user_id"],
        "user_name": user.get("name"),
        "scope": data.get("scope"),
        "expires_in": data.get("expires_in"),
    }


@router.get(
    "/api/v1/developers_keys",
    summary="OAuth2 – List registered mock developer keys",
    tags=["OAuth"],
)
async def list_developer_keys():
    return [{"client_id": cid, "name": v["name"], "redirect_uris": v["redirect_uris"]} for cid, v in REGISTERED_APPS.items()]
