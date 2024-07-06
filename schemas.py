from pydantic import BaseModel
from typing import List, Optional

class SignUp(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_active: bool
    is_staff: bool

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "username": "user7428347t32",
                "email": "mwdkw@gmail.com",
                "password": "12345",
                "is_active": True,
                "is_staff": False,
            }
        }