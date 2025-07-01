from fastapi import APIRouter, Depends
from ..auth import auth_user
from ..models import PromptReq, PromptResp
from ..services.replicate_service import run_llama
from .. import storage

router = APIRouter(prefix="/prompt", tags=["prompt"])

@router.post("/", response_model=PromptResp)
async def ask_llama(data: PromptReq, user: str = Depends(auth_user)):
    answer = await run_llama(data.prompt)
    storage.add(user, data.prompt, answer)
    return {"response": answer}
