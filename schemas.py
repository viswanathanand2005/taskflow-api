from pydantic import BaseModel, ConfigDict,EmailStr
from datetime import datetime,date
from typing import Optional

class UserInput(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    
class UserOutput(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TaskCreate(BaseModel):
    user_id: int
    title: str
    description: str
    status: str = "to_do"
    priority: str = "medium"
    due_date: date

class TaskUpdate(BaseModel):
    user_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None

class TaskOutput(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    status: str
    priority: str
    due_date: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TagCreate(BaseModel):
    name: str

class TagUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class TagOutput(BaseModel):
    id: int
    name: int
    created_at: datetime

class Token(BaseModel):
    accessToken: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
