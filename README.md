# Resume Analyzer - AI-Powered Resume Analysis Tool

A Flask web application that analyzes resumes using AI and provides feedback to help job seekers improve their applications.
## Live Demo
You can check out the live demo of the Resume Analyzer application at [Resume Analyzer Demo](https://ai-resume-analyzer-five.vercel.app/).
## Features

- **AI-Powered Resume Analysis**: Get detailed feedback on your resume using advanced AI models  
- **Job Role Matching**: Check your resume compatibility with specific job positions  
- **ATS Compatibility**: Verify if your resume can pass Applicant Tracking Systems  
- **Resume Management**: Upload, view, and manage multiple resumes  
- **Formatted Resume**: Get professionally formatted versions of your resume  
- **User Authentication**: Secure login and registration system
- **Subscription Plans**: Different plans with varied features (Free, Basic, Premium)
- **User Dashboard**: View and manage your resumes, feedback, and subscription status
- **Responsive Design**: Mobile-friendly interface for easy access on any device


## Technology Stack

- **Backend**: Flask (Python)  
- **Database**: PostgreSQL  
- **Authentication**: JWT authentication with Flask-JWT-Extended
- **AI Integration**: DeepSeek models via OpenRouter API  
- **Frontend**: Bootstrap 5, HTML/CSS, JavaScript

## Local Development

1. **Clone the repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**: Create a `.env` file with the following variables:
   ```env
   API_KEY=your_openrouter_api_key
   SECRET_KEY=your_flask_secret_key
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   ```

4. **Initialize the database:**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **Run the application:**
   ```bash
   flask run
   ```

## Deployment on Vercel

### Prerequisites

- Vercel account  
- PostgreSQL database service (e.g., render.com, Supabase)

### Deployment Steps

1. **Set up a cloud PostgreSQL database**: Create an account with a PostgreSQL provider and get your connection string.

2. **Configure environment variables in Vercel**:
   - `API_KEY`: Your OpenRouter API key  
   - `SECRET_KEY`: Flask secret key  
   - `DATABASE_URL`: Your cloud database connection string

3. **Deploy to Vercel:**
   ```bash
   vercel
   ```

> The project includes a configured `vercel.json` file for seamless deployment.

## Project Structure

```
├── api/
│   ├── app/
│   │   ├── auth.py               # Authentication routes
│   │   ├── models.py             # Database models
│   │   ├── routes.py             # Main application routes
│   │   ├── config.py             # Configuration settings
│   │   ├── services/
│   │   │   └── resume_analyzer.py  # Resume analysis logic
│   │   ├── static/               # Static assets
│   │   └── templates/            # HTML templates
│   ├── index.py                  # Vercel entry point
│   └── requirements.txt          # Project dependencies
├── vercel.json                   # Vercel deployment configuration
└── README.md                     # Project documentation
```

## Authentication

The application uses Flask's session-based authentication:

- User registration with name, email, and password  
- Password encryption using bcrypt  
- Protected routes requiring login  
- Session management for authentication state

## Resume Analysis Features

- Resume scoring (0–100)  
- Content feedback  
- Grammar and style suggestions  
- Job matching recommendations  
- ATS compatibility analysis  
- Skills gap identification
- Formatting suggestions

## API Integration
The application integrates with OpenRouter API to access DeepSeek AI models for resume analysis. This enables advanced natural language processing capabilities for providing accurate and helpful feedback on resumes.

## Contributing
1.Fork the repository
2.Create a feature branch: git checkout -b feature-name
3.Commit your changes: git commit -am 'Add new feature'
4.Push to the branch: git push origin feature-name
5.Submit a pull request