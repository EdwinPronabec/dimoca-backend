from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class SigfoxPayload(BaseModel):
    device: str
    temp: float
    hum: float
    bat: int