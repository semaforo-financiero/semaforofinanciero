from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class MemberResponse(BaseModel):
    user_id: str
    role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

class FamilyWithMembersResponse(BaseModel):
    id: str
    name: str
    created_by: str
    created_at: datetime
    members: List[MemberResponse]

class FamilyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

class FamilyUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

class FamilyInviteCreate(BaseModel):
    email: EmailStr

class AcceptInvitation(BaseModel):
    family_id: str
    
class RejectInvitation(BaseModel):
    family_id: str
