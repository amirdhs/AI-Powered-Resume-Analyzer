# AI-Powered Resume Analyzer

AI-Powered Resume Analyzer is a web application built using the Flask framework in Python. The application allows users to upload their resumes in PDF format, which are then analyzed by an AI to provide feedback and suggestions for improvement.

## Features

- User registration and login
- Upload resumes in PDF format
- Analyze resumes using AI
- Provide feedback and suggestions for improvement
- View and download analyzed resumes
- Delete resumes

## Project Structure

- `app.py`: The main entry point of the application. It initializes the Flask app and sets up the database.
- `app/models.py`: Defines the database models for `User` and `Resume`.
- `app/routes.py`: Contains the main routes for the application, including the dashboard, resume upload, and analysis.
- `app/auth.py`: Handles user authentication, including registration and login.
- `app/config.py`: Configuration settings for the Flask app, including database and JWT settings.
- `app/services/resume_analyzer.py`: Contains the logic for extracting text from PDF resumes and analyzing them using an AI API.
- `app/templates/`: Directory containing HTML templates for rendering the web pages.
- `app/static/`: Directory for static files like CSS, JavaScript, and images.
- `requirements.txt`: Lists the Python dependencies required for the project.
- `vercel.json`: Configuration file for deploying the application on Vercel.
- `.env`: Environment variables for sensitive information like API keys and database URLs.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ai-powered-resume-analyzer.git
    cd ai-powered-resume-analyzer
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    ```sh
    cp .env.example .env
    ```

5. Update the `.env` file with your API keys and database URL.

6. Initialize the database:
    ```sh
    flask db upgrade
    ```

7. Run the application:
    ```sh
    flask run
    ```

## Usage

1. Register a new user account.
2. Log in with your credentials.
3. Upload a resume in PDF format.
4. View the analysis results and feedback.
5. Download or delete the analyzed resume.

## Configuration

- `app/config.py`: Loads environment variables and sets configuration options for the Flask app.
- `vercel.json`: Configures the deployment on Vercel, specifying the build settings and routes.

## Deployment

To deploy the application on Vercel, follow these steps:

1. Install the Vercel CLI:
    ```sh
    npm install -g vercel
    ```

2. Deploy the application:
    ```sh
    vercel
    ```

## Dependencies

- Flask and various Flask extensions (e.g., Flask-SQLAlchemy, Flask-Migrate, Flask-JWT-Extended)
- SQLAlchemy for ORM
- `PyPDF2` for PDF text extraction
- `requests` for making API calls
- `bcrypt` for password hashing
- Google APIs for additional functionalities

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.