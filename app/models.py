from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class LoginReq(BaseModel):
    username: str
    password: str

class TokenResp(BaseModel):
    access_token: str = Field(..., alias="token")

class PromptReq(BaseModel):
    prompt: str

class PromptResp(BaseModel):
    response: str

class HistItem(BaseModel):
    timestamp: datetime
    prompt: str
    response: str

class HistResp(BaseModel):
    history: List[HistItem]
