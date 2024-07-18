from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Form

from faceValidation import validation

import os

app = FastAPI()

# Define the request body

class ProfileData(BaseModel):
    age: Optional[int] = None
    gender: str = "male"
    verify_age: bool = False
    slack: float = 0.25

# Endpoint for photo validation

@app.post("/validate_profile_photo")
async def validate_profile_photo(
    age: Optional[int] = Form(None),
    gender: str = Form("male"),
    slack: float = Form(0.25),
    photo: UploadFile = File(...)
    ):
   
    # Save the uploaded file to the "images" folder in the current directory
    save_path = os.path.join(os.getcwd(), "images", photo.filename)
    with open(save_path, "wb") as buffer:
        buffer.write(await photo.read())
    
    # print(save_path)

    resp = validation(save_path, age, gender, slack)
    print(resp)
    return {"response": resp}   
    

    # return {"age": age, "gender": gender, "slack": slack, "filename": save_path}
