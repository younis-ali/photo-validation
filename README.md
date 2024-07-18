# Photo Validation API

This FastAPI application allows users to upload a profile photo and validate the user's age and gender, with an optional age verification flag.

## Features

- Upload a profile photo
- Validate user's age and gender
- Optional age parameter, if given then age will be detected otherwise not

## Requirements

- Python 3.7+
- FastAPI
- Pydantic
- Uvicorn

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/photo-validation.git
    cd photo-validation
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` should include:
    ```
    fastapi
    uvicorn
    ```

## Running the Application

1. Start the FastAPI application using Uvicorn:

    ```bash
    uvicorn main:app --reload
    ```

    The endpoints will be available at `http://127.0.0.1:8000/docs`.

## Usage

### Endpoint: `/validate_profile_photo`

**Method:** POST

**Description:** Validate the user's profile photo, age, gender, and optionally verify the age.

**Request:**
  - `photo` (UploadFile): The profile photo file.
  - `age` (int): The user's age optional.
  - `gender` (str): The user's gender. Must be either "Male" or "Female".
  - `slack` (bool): predicted age flexibility value. Default is `0.25`.

**Example Request:**

- When `age` is `Given`
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/validate_profile_photo' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'age=42' \
  -F 'gender=' \
  -F 'slack=0.80' \
  -F 'photo=@photograph.jpg;type=image/jpeg'
  ```
  Resonse Body
  ```json
  {
    "response": {
      "message": "Profile photo successfully varified",
      "is_valid": true,
      "number_of_faces": 1,
      "predicted_age_range": "(50-60)",
      "predicted_gender": "male"
    }
  }
```


- When `age` is none
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/validate_profile_photo' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'age=' \
  -F 'gender=male' \
  -F 'slack=0.25' \
  -F 'photo=@photograph.jpg;type=image/jpeg'
  ```
Response Body
```json
{
  "response": {
    "message": "Profile photo successfully varified",
    "is_valid": true,
    "number_of_faces": 1,
    "predicted_gender": "male"
  }
}
```
Some more examples of responses in different senarios

- When non-human face image is given

```json
{
  "response": {
    "message": "No face detected or multiple faces detected.",
    "is_valid": false
  }
}
```
- When predicted age does not matches with given age
```json
{
  "response": {
    "message": "Profile photo not verified because the predicted age is outside the acceptable range. You can reconfigure the slack value",
    "is_valid": false,
    "number_of_faces": 1,
    "predicted_age_range": "(50-60)",
    "predicted_gender": "male"
  }
}
```

- When predicted gender does not matches with given gender
``` json
{
  "response": {
    "message": "Profile photo not verified because the predicted gender does not match the given gender value",
    "is_valid": false,
    "number_of_faces": 1,
    "predicted_age_range": "(50-60)",
    "predicted_gender": "male"
  }
}
```