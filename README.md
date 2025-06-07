# Issue Management Application

This project is a simple application to help users manage issues in their daily work. It allows for recording issues, tracking discussions, and documenting solutions.

## Features

*   Record detailed information about issues (what, where, when, system, consequence, responsibility).
*   Log discussions related to each issue.
*   Document final solutions, estimated deadlines, and responsible parties.
*   Separate frontend and backend architecture with a PostgreSQL database.

## Project Structure

*   `/frontend`: Contains the React frontend application.
*   `/backend`: Contains the Flask backend API.
*   `/database`: Contains database schema design (`schema.md`).

## Setup Instructions

### Backend

1.  **Navigate to the `backend` directory:**
    ```bash
    cd backend
    ```
2.  **Create a Python virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up PostgreSQL Database:**
    *   Ensure PostgreSQL is installed and running.
    *   Create a user (e.g., `swebot`) and a database (e.g., `issue_tracker_db`).
        ```sql
        -- Example SQL commands:
        -- CREATE USER swebot WITH PASSWORD 'password';
        -- CREATE DATABASE issue_tracker_db OWNER swebot;
        ```
    *   Configure the database URI in `backend/app.py` (currently set to `postgresql://swebot:password@localhost:5432/issue_tracker_db`).
5.  **Initialize the database tables:**
    Set the `PYTHONPATH` and `FLASK_APP` environment variables first (from the project root or adjust paths accordingly):
    ```bash
    export PYTHONPATH=.  # Assuming you are in the project root, or /app if in a container
    export FLASK_APP=backend.app
    flask init-db
    ```
    (If you are in the `backend` directory, `PYTHONPATH=..` might be needed if `backend` is not a package itself relative to a root `PYTHONPATH`.)
    A common setup if running from project root: `PYTHONPATH=. FLASK_APP=backend.app flask init-db`

6.  **Run the backend server:**
    ```bash
    flask run --host=0.0.0.0 --port=5000
    ```
    The API will be available at `http://localhost:5000`.

### Frontend

1.  **Navigate to the `frontend` directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run the frontend development server:**
    ```bash
    npm start
    ```
    The application will typically open in your browser at `http://localhost:3000`. The frontend is configured to proxy API requests to the backend (running on port 5000).

## API

The backend provides a RESTful API for managing issues, discussions, and solutions.
For detailed API endpoint documentation, please see `backend/api_design.md`.

## Testing

### Backend Unit Tests

1.  **Ensure PostgreSQL is running and a test database (e.g., `issue_tracker_test_db`) is created and accessible** by the same user configured for the main database.
    ```sql
    -- Example SQL commands:
    -- CREATE DATABASE issue_tracker_test_db OWNER swebot;
    ```
2.  **Navigate to the project root (or ensure `PYTHONPATH` is set up correctly).**
3.  **Run the tests:**
    Set the `PYTHONPATH` and `FLASK_APP` (if not already set in your environment):
    ```bash
    export PYTHONPATH=.
    export FLASK_APP=backend.app
    python -m unittest discover backend/tests -v
    ```
