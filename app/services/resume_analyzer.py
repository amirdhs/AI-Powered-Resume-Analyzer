import requests
import PyPDF2
import json
import os
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API key not found. Please set the API_KEY environment variable.")


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            pdf = PyPDF2.PdfReader(file)
            text = "".join(page.extract_text() or "" for page in pdf.pages)
        return text
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
        exit(1)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        exit(1)


# OpenRouter API Configuration
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def analyze_resume(resume_text):
    # Define the prompt for resume analysis
    prompt = f"""[SYSTEM: You are a resume analysis AI that must respond with valid JSON only. Do not explain, just output the JSON.]

    Analyze this resume text for language quality:
    {resume_text}

    RESPOND WITH THIS JSON ONLY:
    {{
        "score": <number 0-100>,
        "feedback": "<concise feedback>",
        "best_match": "<best matching job title>",
        "ats_compatibility": "<feedback on ATS compatibility>",
        "suggestions": "<Overall suggestions>",
        "formatted_resume": "<Corrected {resume_text} and rewrite it in a professional manner and HTML format.make score 100>",
        "improvement_suggestions": {{
            "Grammar": ["Fix subject-verb agreement", "Use active voice"],
            "Formatting": ["Use consistent bullet points", "Add section headings"],
            "Content": ["Add quantifiable achievements", "Tailor for specific job roles"]
        }},
        "best_jobs": [
            {{
                "title": "<job title>",
                "match_score": <number 0-100>,
                "matching_skills": ["skill1", "skill2"],
                "missing_skills": ["skill3", "skill4"],
                "recommendations": ["Add skill3", "Highlight skill1"],
                "description": "<job description>"
            }}
        ]
    }}
    """

    # Call OpenRouter AI API
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
                "X-Title": "<YOUR_SITE_NAME>",  # Optional
            },
            extra_body={},
            model="deepseek/deepseek-r1-distill-qwen-32b:free",
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse JSON response
        response_text = completion.choices[0].message.content.strip()

        # Remove backticks if they exist
        if response_text.startswith("```json") and response_text.endswith("```"):
            response_text = response_text[7:-3].strip()

        try:
            response_json = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return {
                "score": 0,
                "feedback": "Error analyzing resume.",
                "best_match": "N/A",
                "ats_compatibility": "N/A",
                "suggestions": "N/A",
                "formatted_resume": "N/A",
                "improvement_suggestions": {},
                "best_jobs": []
            }

        # Return the feedback as a dictionary
        return response_json

    except requests.exceptions.RequestException as e:
        print(f"Error sending request to the API: {e}")
        return {
            "score": 0,
            "feedback": "Error analyzing resume.",
            "best_match": "N/A",
            "ats_compatibility": "N/A",
            "suggestions": "N/A",
            "formatted_resume": "N/A",
            "improvement_suggestions": {},
            "best_jobs": []
        }

def check_for_job(resume_text,job_role):
    # Define the prompt for job role analysis
    prompt = f"""[SYSTEM: You are a resume analysis AI that must respond with valid JSON only. Do not explain, just output the JSON.]

    Considering the background, education, and skills, is this job {job_role} role best suit for this resume {resume_text}?

    RESPOND WITH THIS JSON ONLY:
    {{
        "job_role": "<job role>",
        "suitability_score": <number 0-100>,
        "recommendations": "<concise feedback>"
    }}
    """

    # Call OpenRouter AI API
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
                "X-Title": "<YOUR_SITE_NAME>",  # Optional
            },
            extra_body={},
            model="deepseek/deepseek-r1-distill-qwen-32b:free",
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse JSON response
        response_text = completion.choices[0].message.content.strip()

        # Remove backticks if they exist
        if response_text.startswith("```json") and response_text.endswith("```"):
            response_text = response_text[7:-3].strip()

        try:
            response_json = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return {
                "job_role": "N/A",
                "suitability_score": 0,
                "recommendations": "Error analyzing resume."
            }

        # Return the feedback as a dictionary
        return response_json

    except requests.exceptions.RequestException as e:
        print(f"Error sending request to the API: {e}")
        return {
            "job_role": "N/A",
            "suitability_score": 0,
            "recommendations": "Error analyzing resume."
        }