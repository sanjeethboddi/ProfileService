import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

# - [GET]/getDisplayName(userId) —> String displayName
# - [GET]/getDateOfBirth(userId) —> Date dateOfBirth
# - [GET]/getAddress(userId) —> Location address
# - [GET]/getFollowersCount(userId) —> Long followersCount
# - [GET]/getFollowingCount(userId) —> Long followingCount
# - [GET]/getPetsList(userId) —> List<PetIds> petsList
# - [PUT]/setDisplayName(userId, displayName) —> None
# - [PUT]/setDateOfBirth(userId, dateOfBirth) —> None
# - [PUT]/setAddress(userId, address) —> None
# - [POST]/createProfile(userId, displayName, dateOfBirth, address) —> None

class Profile(BaseModel):
    uid: str = Field(alias="_id")
    displayName: str = Field(...)
    dateOfBirth: str = Field(...)
    address: str = Field(...)
    followersCount: int = Field(...)
    followingCount: int = Field(...)
    petsList: list = Field(...)


    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "sanjeethboddi",
                "displayName": "Sanjeeth Boddinagula",
                "dateOfBirth": "1997-01-01",
                "address": "1234 Main St, San Jose, CA 95112",
                "followersCount": 0,
                "followingCount": 0,
                "petsList": []
            }
        }

class ProfileUpdate(BaseModel):
    displayName: str = Field(...)
    dateOfBirth: datetime = Field(...)
    address: str = Field(...)
    followersCount: int = Field(...)
    followingCount: int = Field(...)
    petsList: list = Field(...)


    class Config:
        schema_extra = {
            "example": {
                "displayName": "Sanjeeth Boddinagula",
                "dateOfBirth": "1997-01-01",
                "address": "1234 Main St, San Jose, CA 95112",
                "petsList": []
            }
        }
