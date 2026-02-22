from pydantic import BaseModel, EmailStr, Field

class FamilyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

class FamilyInviteCreate(BaseModel):
    email: EmailStr

class AcceptInvitation(BaseModel):
    token: str