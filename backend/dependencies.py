from fastapi import HTTPException, Cookie, Depends, Request
from jose import jwt, JWTError
import requests
from typing import Annotated

from config import settings
from models import *
from database import Database


def get_current_user(db: Database, session_id: str = Cookie(None)):
    try:
        payload = jwt.decode(session_id, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid session_id")
    else:
        db_user = db.get(User, payload["user_id"])
        return db_user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_verify_user(db: Database, request: Request, token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM, audience=request.scope["route"].name)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    else:
        db_user = db.get(User, payload["user_id"])
        return db_user

VerifyUser = Annotated[User, Depends(get_verify_user)]

def verify_turnstile_token(turnstile_token: str = None):
    return
    body = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": turnstile_token,
    }
    r = requests.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", json=body)
    if not r.json()["success"]:
        raise HTTPException(status_code=403, detail="Invalid captcha token")