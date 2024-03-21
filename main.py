from fastapi import FastAPI, File, UploadFile, Form
from faceValidation import validate_profile_photo
import os

app = FastAPI()

@app.post("/validate_profile_photo")
async def validate_photo_endpoint(photo: UploadFile = File(...), age: int = Form(...), gender: str = Form(...)):
   
    # Save the uploaded file to the "images" folder in the current directory
    save_path = os.path.join(os.getcwd(), "images", photo.filename)
    with open(save_path, "wb") as buffer:
        buffer.write(await photo.read())
    
    print(save_path)
 
    result = validate_profile_photo(save_path, age, gender)
    return {"result": result}

