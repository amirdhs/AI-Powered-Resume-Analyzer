import requests
import PyPDF2
import json  # Import the json module to parse the embedded JSON string

from googleapiclient.mimeparse import best_match


def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, "rb") as file:
        # Create a PDF file reader
        pdf = PyPDF2.PdfReader(file)

        # Initialize an empty string to store the text
        text = ""

        # Iterate over each page
        for page_num in range(len(pdf.pages)):
            # Extract the text from the page
            text += pdf.pages[page_num].extract_text()
        return text

# Define the API endpoint
API_URL = "http://localhost:11434/api/generate"

# Extract text from the PDF
pdf_path = "resume.pdf"  # Replace with the actual path to your PDF
try:
    text = extract_text_from_pdf(pdf_path)
except FileNotFoundError:
    print(f"Error: The file '{pdf_path}' was not found.")
    exit(1)
except Exception as e:
    print(f"Error extracting text from PDF: {e}")
    exit(1)

# Define the payload with the model name and the prompt
payload = {
    "model": "llama3.2:latest",  # Replace with your model name
    "prompt": f"""[SYSTEM: You are a resume analysis API that must respond with valid JSON only. Do not explain, just output the JSON.]

        Analyze this resume text for language quality:
        {text}

        Consider:
        - Professional tone
        - Clear communication
        - Active voice usage
        - Consistency in formatting

        RESPOND WITH THIS JSON ONLY:
        {{
            "score": <number 0-100>,
            "feedback": "<concise feedback>"
            "best_match": "<best matching job title>"
            "ats_compatibility": "<feedback on ATS compatibility>"
            "suggestions": "<Overall suggestions>"
        }}
        """,
    "stream": False
}

# Send a POST request to the API
try:
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
except requests.exceptions.RequestException as e:
    print(f"Error sending request to the API: {e}")
    exit(1)

# Check if the request was successful
if response.status_code == 200:
    try:
        # Parse the JSON response
        result = response.json()

        # Extract the embedded JSON string from the 'response' field
        response_json = json.loads(result["response"])

        # Extract the score and feedback from the parsed JSON
        score = response_json.get("score")
        feedback = response_json.get("feedback")
        best_job_match = response_json.get("best_match")
        ats_compatibility = response_json.get("ats_compatibility")
        suggestions = response_json.get("suggestions")

        if score is not None and feedback is not None:
            print(f"Score: {score}")
            print(f"Feedback: {feedback}")
            print(f"Best matching job title: {best_job_match}")
            print(f"ATS compatibility: {ats_compatibility}")
            print(f"Suggestions for improving resume: {suggestions}")
        else:
            print("Error: The response does not contain the expected 'score' or 'feedback' fields.")
            print("Full response:", response_json)
    except (ValueError, KeyError) as e:
        print(f"Error parsing JSON response: {e}")
        print("Raw response:", response.text)
else:
    print(f"Failed to get a response: {response.status_code}")
    print("Response text:", response.text)