from fastapi import APIRouter, Depends
from ..auth import auth_user
from ..models import HistResp
from .. import storage

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/", response_model=HistResp)
def get_history(user: str = Depends(auth_user)):
    return {"history": storage.get(user)}
