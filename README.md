# Resume Analyzer

## Overview
Resume Analyzer is a web application that allows users to upload their resumes, receive AI-generated feedback, and manage their uploaded resumes. The application provides functionalities for user registration, login, dashboard access, resume upload, analysis, and deletion.

## Features
- **User Registration and Login**: Secure user authentication.
- **Dashboard**: Displays user-specific options to upload and analyze resumes.
- **Resume Upload**: Users can upload their resumes in PDF format for analysis.
- **AI Feedback**: Provides feedback on the uploaded resume, including score, best matching job title, ATS compatibility, and suggestions.
- **Resume Management**: Users can view and delete their uploaded resumes.
- **Logout**: Securely logs out the user.

## Endpoints
### `/login`
- **POST**: User login with email and password.
  - **Responses**:
    - `200`: User logged in successfully.
    - `400`: Invalid credentials.

### `/dashboard`
- **GET**: Displays the user's dashboard.
  - **Responses**:
    - `200`: Dashboard displayed successfully.
    - `401`: User not logged in.
- **POST**: Upload and analyze resume.
  - **Request Body**: `multipart/form-data` with `resume` (PDF file).
  - **Responses**:
    - `200`: Resume analyzed successfully.
    - `400`: Invalid file type or no file uploaded.

### `/delete_resume/{resume_id}`
- **DELETE**: Deletes a specific resume by its ID.
  - **Parameters**: `resume_id` (integer, required).
  - **Responses**:
    - `200`: Resume deleted successfully.
    - `401`: User not logged in.
    - `403`: User does not have permission to delete this resume.
    - `404`: Resume not found.

### `/logout`
- **GET**: Logs out the currently logged-in user.
  - **Responses**:
    - `200`: User logged out successfully.

## Technologies Used
- **Python**
- **Flask**: Web framework.
- **Bootstrap**: Frontend framework for responsive design.


