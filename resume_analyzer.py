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
        "suggestions": "<Overall suggestions>"
        "formatted_resume": "<Corrected resume text and rewrite it in a professional manner and HTML format>"
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
            exit(1)

        # Return the feedback as a dictionary
        return response_json

    except requests.exceptions.RequestException as e:
        print(f"Error sending request to the API: {e}")
    except (ValueError, KeyError) as e:
        print(f"Error parsing JSON response: {e}")