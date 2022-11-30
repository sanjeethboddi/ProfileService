from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models.profile import Profile, ProfileUpdate

router = APIRouter()

db_name = "profiles"

@router.post("/", response_description="Create a new profile", status_code=status.HTTP_201_CREATED, response_model=Profile)
def create_profile(request: Request, profile: Profile = Body(...)):
    profile = jsonable_encoder(profile)
    new_book = request.app.database[db_name].insert_one(profile)
    created_profile = request.app.database[db_name].find_one(
        {"_id": new_book.inserted_id}
    )
    return created_profile

@router.get("/", response_description="List all profiles", response_model=List[Profile])
def list_profiles(request: Request):
    books = list(request.app.database[db_name].find(limit=100))
    return books

@router.get("/{id}", response_description="Get a single profile by id", response_model=Profile)
def find_profile(id: str, request: Request):
    if (book := request.app.database[db_name].find_one({"_id": id})) is not None:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

@router.put("/{id}", response_description="Update a profile", response_model=Profile)
def update_profile(id: str, request: Request, profile: ProfileUpdate = Body(...)):
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



@router.delete("/{id}", response_description="Delete a book")
def delete_profile(id: str, request: Request, response: Response):
    delete_result = request.app.database[db_name].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Profile with ID {id} not found")



