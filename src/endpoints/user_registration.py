from fastapi import APIRouter, UploadFile,Depends,File, HTTPException
from src.schemas.register_schema import User_Registration
from sqlalchemy.orm import Session
from src.common.connect_db import get_db
from src.models.postgres_orm_model import User

router=APIRouter(tags=["User Registration"])

@router.post('/register')
async def register_user(userinfo : User_Registration = Depends(),profile_picture : UploadFile = File(...),db: Session = Depends(get_db)):
    """
    API to register the users
    This endpoint allows users to register by providing their full name, email, password, phone, and an optional profile picture.
    """
    user_email = db.query(User.id).filter(User.Email==userinfo.email).first()
    user_phone = db.query(User.id).filter(User.Phone==userinfo.phone).first()
    if user_email is not None:
        raise HTTPException(status_code=409,detail={"message":"Email already exists","statusCode": 409,"errorCode": None})
    elif user_phone is not None:
        raise HTTPException(status_code=409,detail={"message":"Phone number already exists","statusCode": 409,"errorCode": None})
    else:
        user_details = User(FirstName = userinfo.fullname, password = userinfo.password , Email = userinfo.email, Phone = userinfo.phone)
        db.add(user_details)
        db.commit()
        db.refresh(user_details)
        return {"detail": {"message": "User details added successfully.", "statusCode": 201, "errorCode": None}} 
