from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Dict

_USERS: Dict[str, Dict] = {
    "alice": {"password": "secret1", "token": "token_alice"},
    "bob":   {"password": "secret2", "token": "token_bob"},
}
_TOKEN_TO_USER = {v["token"]: k for k, v in _USERS.items()}

_bearer = HTTPBearer(auto_error=False)

def auth_user(creds: HTTPAuthorizationCredentials = Security(_bearer)) -> str:
    if not creds:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing token")
    token = creds.credentials
    user = _TOKEN_TO_USER.get(token)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    return user

def login(username: str, password: str) -> str:
    rec = _USERS.get(username)
    if not rec or rec["password"] != password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Bad username/password")
    return rec["token"]
