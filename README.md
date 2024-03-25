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
