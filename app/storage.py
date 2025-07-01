# app/storage.py
import json, threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List

_file  = Path("history.json")
_lock  = threading.Lock()
_cache: Dict[str, List[dict]] = {}

def _save_to_disk() -> None:
    # called only when _lock is already held
    _file.write_text(json.dumps(_cache, indent=2, default=str))

def add(user: str, prompt: str, answer: str) -> None:
    rec = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "response": answer,
    }
    with _lock:
        _cache.setdefault(user, []).append(rec)
        _save_to_disk()                 # no second lock acquisition

def get(user: str) -> List[dict]:
    if not _cache and _file.exists():
        with _lock:
            _cache.update(json.loads(_file.read_text()))
    return _cache.get(user, [])
