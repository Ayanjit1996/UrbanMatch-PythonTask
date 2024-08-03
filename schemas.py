from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
from email_validator import validate_email, EmailNotValidError

class UserBase(BaseModel):
    name: str
    age: int
    gender: str
    email: EmailStr
    city: str
    interests: List[str]

    @field_validator('email')
    def validate_email(cls, email: str):
        try:
            validate_email(email)
            return email
        except EmailNotValidError:
            raise ValueError("Invalid email address")

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    city: Optional[str] = None
    interests: Optional[List[str]] = None

    @field_validator('interests', mode='before')
    def check_interests(cls, interests: Optional[List[str]]):
        if interests is None:
            return []
        return interests

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True