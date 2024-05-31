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

- When `age` is `None`
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/validate_profile_photo' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'age=' \
  -F 'gender=male' \
  -F 'slack=0.25' \
  -F 'photo=@pexels-pixabay-415829.jpg;type=image/jpeg'
  ```
  Resonse Body
  ```json
  {
  "response": {
    "is_valid": true,
    "number_of_faces": 1,
    "predicted_gender": "male"
  }
}
```


- When `age` is given
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/validate_profile_photo' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'age=45' \
  -F 'gender=male' \
  -F 'slack=0.25' \
  -F 'photo=@pexels-pixabay-415829.jpg;type=image/jpeg'
  ```
Response Body
```json
{
  "response": {
    "is_valid": false,
    "number_of_faces": 1,
    "predicted_age_range": "(20-30)",
    "predicted_gender": "male"
  }
}
```
- When non-human face image is given
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/validate_profile_photo' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'age=' \
  -F 'gender=male' \
  -F 'slack=0.25' \
  -F 'photo=@dog.png;type=image/png'
```
- Response Body
```json
{
  "response": {
    "message": "No face detected or multiple faces detected.",
    "is_valid": false
  }
}
```