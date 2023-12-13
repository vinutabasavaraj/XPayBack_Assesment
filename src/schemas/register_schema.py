from typing import Optional
from typing import List
from pydantic import AnyUrl, BaseModel, Field
from fastapi import  UploadFile, File


class User_Registration(BaseModel):
    fullname : str = Field(example="Fullname",min_length=1)
    email : str = Field(example="email",min_length=1)
    password: str = Field(example="password",min_length=1)
    phone : int = Field(example="phone")
    
    
