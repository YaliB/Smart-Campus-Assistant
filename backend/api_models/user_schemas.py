from pydantic import BaseModel
from typing import Optional

# Schema for incoming data (Creating a user)
class UserCreate(BaseModel):
    email: str
    password: str
    student_id: Optional[str] = None
    is_admin: bool = False

# Schema for outgoing data (Returning user data - NEVER return password!)
class UserResponse(BaseModel):
    id: int
    email: str
    student_id: Optional[str] = None
    is_admin: bool

    class Config:
        from_attributes = True

# Schema for updating user data (Partial updates allowed)
class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    student_id: Optional[str] = None
    is_admin: Optional[bool] = None