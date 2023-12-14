from typing import Optional
from typing import List
from pydantic import BaseModel, Field, EmailStr,constr
from fastapi import  UploadFile, File


class User_Registration(BaseModel):
    fullname : str = Field(example="Fullname",min_length=1)
    email : EmailStr = Field(example="email")
    password: str = Field(example="password",min_length=1)
    phone: constr(regex=r"^[0-9]{10}$")
    
    
