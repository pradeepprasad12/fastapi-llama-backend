from fastapi import APIRouter
from ..auth import login
from ..models import LoginReq, TokenResp

router = APIRouter(prefix="/login", tags=["auth"])

@router.post("/", response_model=TokenResp)
def do_login(data: LoginReq):
    token = login(data.username, data.password)
    return {"token": token}
