from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

try:
    from firebase_admin import auth
except ModuleNotFoundError:  # pragma: no cover - optional dependency in offline mode
    auth = None

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if credentials is None or not credentials.credentials:
        return {"uid": "anonymous", "email": None, "is_guest": True}

    if auth is None:
        return {"uid": "anonymous", "email": None, "is_guest": True}

    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
    except Exception as exc:  # pragma: no cover - runtime validation path
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase token",
        ) from exc

    return decoded_token
