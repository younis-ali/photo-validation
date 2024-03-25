# Profile Photo Validation API

## Usage

1. Create a virtual environment:

    ```bash
    python3 -m venv .venv
    ```

2. Activate the virtual environment:

    - On Linux/macOS:

        ```bash
        source .venv/bin/activate
        ```

    - On Windows:

        ```bash
        .venv\Scripts\activate
        ```

3. Upgrade pip:

    ```bash
    pip install --upgrade pip
    ```

4. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the API:

    ```bash
    uvicorn app:app --reload
    ```

6. Access the API documentation at http://localhost:8000/docs.

## API Response

The API response will be in the following format:

```json
{
  "response": {
    "number_of_faces": 1,
    "predicted_age": "(20-30)",
    "predicted_gender": "Male",
    "is_valid": true
  }
}
Where:

number_of_faces: The number of faces detected in the uploaded photo.
predicted_age: The predicted age range of the person in the photo.
predicted_gender: The predicted gender of the person in the photo.
is_valid: A boolean indicating whether the profile photo is valid or not.

