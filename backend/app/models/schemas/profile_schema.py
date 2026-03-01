from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class SocioeconomicProfileUpsertRequest(BaseModel):
    age: int = Field(ge=0, le=120)
    years_working: int = Field(ge=0, le=80)
    gender: str = Field(min_length=1, max_length=30)
    state: str = Field(min_length=1, max_length=60)
    employment_status: str = Field(min_length=1, max_length=30)
    education_level: str = Field(min_length=1, max_length=30)
    job_title: str = Field(min_length=1, max_length=30)


class SocioeconomicProfileResponse(BaseModel):
    id: str
    age: int
    years_working: int
    gender: str
    state: str
    employment_status: str
    education_level: str
    job_title: str 


class BasicProfileResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str


class ProfileResponse(BaseModel):
    profile: BasicProfileResponse
    socioeconomic_profile: Optional["SocioeconomicProfileResponse"] = None