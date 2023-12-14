from fastapi import APIRouter, UploadFile,Depends,File, HTTPException
from src.schemas.register_schema import User_Registration
from sqlalchemy.orm import Session
from pathlib import Path
import base64
from passlib.hash import bcrypt

from src.common.connect_db import get_db
from src.models.postgres_orm_model import User, Profile

router=APIRouter(tags=["User Registration"])

#API to create user
@router.post('/user')
async def register_user(userinfo : User_Registration = Depends(),profile_picture : UploadFile = File(...),db: Session = Depends(get_db)):
    """
    API to register the users
    This endpoint allows users to register by providing their full name, email, password, phone, and an optional profile picture.
    """
    
    user_email = db.query(User.id).filter(User.Email==userinfo.email).first()
    user_phone = db.query(User.id).filter(User.Phone==userinfo.phone).first()
    
    hashed_password = bcrypt.hash(userinfo.password)

    if user_email is not None:
        raise HTTPException(status_code=409,detail={"message":"Email already exists","statusCode": 409,"errorCode": None})
    elif user_phone is not None:
        raise HTTPException(status_code=409,detail={"message":"Phone number already exists","statusCode": 409,"errorCode": None})
    else:
        user_details = User(FirstName = userinfo.fullname, password = hashed_password , Email = userinfo.email, Phone = userinfo.phone)
        db.add(user_details)
        db.commit()
        db.refresh(user_details)
        
        user_id = db.query(User.id).filter(User.Email==userinfo.email).first()
        print(user_id.id)
        
        cwd = Path(__file__).parents[2]
        image_folder_path = cwd/'images'/ str(profile_picture.filename)
        
        with open(image_folder_path, "wb") as f:
            f.write(profile_picture.file.read())
            
        file_extension = profile_picture.filename.split(".")[-1]
        
        image_filepath = str(image_folder_path)
        
        user_profile = Profile(profile_picture = image_filepath, profile_picture_name = profile_picture.filename , extension = file_extension, user_id = user_id.id)
        db.add(user_profile)
        db.commit()
        db.refresh(user_profile)
                
    return {"detail": {"message": "User details added successfully.", "statusCode": 201, "errorCode": None}} 

#API to fetch the user details
@router.get('/user')
async def user_details(db: Session = Depends(get_db)):
    """
    API to fetch all the users details
    """
    user_profiles = []
    result = db.query(User, Profile).join(Profile, User.id == Profile.user_id).all()
    for user, profile in result:
        user_data = {
            "user_id":user.id,
            "user_name":user.FirstName,
            "user_email":user.Email,
            "profile_id":profile.id,
            "picture_name":profile.profile_picture_name,
            "extension":profile.extension
        }
        user_profiles.append(user_data)
        
    return {"detail":{"message":"user deatils fetched successfully","data":user_profiles,"statusCode": 200,"errorCode": None}}