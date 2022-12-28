from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Profile, ProfileUpdate
import requests

router = APIRouter()

db_name = "profiles"

# @router.post("/callAuth")
# def callAuth(request: Request, token: str):
#     resp =  requests.post(request.app.auth_service+f"/verify/{token}")
#     return resp.json()

@router.post("/{token}", response_description="Create a new profile", status_code=status.HTTP_201_CREATED, response_model=Profile)
def create_profile(request: Request, token:str, profile: Profile = Body(...)):
    resp =  requests.post(request.app.auth_service+f"/verify/{token}")
    uid = profile.uid
    if  resp.status_code != 200 or resp.json()["username"] != uid:
        raise HTTPException(status_code=401, detail="Unauthorized")
    profile_json = jsonable_encoder(profile)
    # find if uid exists
    if request.app.database[db_name].find_one({"_id": uid}):
        raise HTTPException(status_code=409, detail="Profile already exists")
    new_book = request.app.database[db_name].insert_one(profile_json)
    requests.post(request.app.graph_service+f"/createUser/{token}", json={"uid": uid})
    created_profile = request.app.database[db_name].find_one(
        {"_id": new_book.inserted_id}
    )
    return created_profile

@router.get("/", response_description="List all profiles", response_model=List[Profile])
def list_profiles(request: Request, response: Response):
    profiles = list(request.app.database[db_name].find(limit=100))
    if profiles:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return profiles

@router.get("/{id}", response_description="Get a single profile by id", response_model=Profile)
def find_profile(id: str, request: Request):
    if (profile := request.app.database[db_name].find_one({"_id": id})) is not None:
        return profile
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Profile with ID {id} not found")

@router.put("/{id}/{token}", response_description="Update a profile", response_model=Profile)
def update_profile(id: str, request: Request, token:str, profile: ProfileUpdate = Body(...)):
    id = id.lower()
    resp =  requests.post(request.app.auth_service+f"/verify/{token}")
    if not resp.ok or resp.json()["username"] != id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    profile = {k: v for k, v in profile.dict().items() if v is not None}
    if len(profile) >= 1:
        update_result = request.app.database[db_name].update_one(
            {"_id": id}, {"$set": profile}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Profile with ID {id} not found")

    if (
        existing_profile := request.app.database[db_name].find_one({"_id": id})
    ) is not None:
        return existing_profile

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Profile with ID {id} not found")



@router.delete("/{id}/{token}", response_description="Delete a book")
def delete_profile(id: str, token:str, request: Request, response: Response):
    id = id.lower()
    resp =  requests.post(request.app.auth_service+f"/verify/{token}")
    if not resp.ok  or resp.json()["username"] != id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    delete_result = request.app.database[db_name].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        requests.post(request.app.graph_service+f"/deleteUser/{token}", json={"uid": id})
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Profile with ID {id} not found")



