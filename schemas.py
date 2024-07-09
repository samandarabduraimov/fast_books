from typing_extensions import Self
from pydantic import BaseModel
from typing import List, Optional, Any

class SignUp(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_active: bool
    is_staff: bool


class LoginModel(BaseModel):
    username: str
    password: str

class Settings(BaseModel):
    authjwt_secret_key: str = "76ce38ef876902afa65ba6b260015efd40abe3ff251ccc5381ab876baba93364"