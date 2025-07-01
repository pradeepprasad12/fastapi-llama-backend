from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from .routers import auth, prompt, history

app = FastAPI(title="FastAPI‑Replicate Backend")

app.include_router(auth.router)
app.include_router(prompt.router)
app.include_router(history.router)
