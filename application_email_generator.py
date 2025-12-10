import os
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
import logging
from prompts import SYSTEM_PROMPT, build_user_prompt
logger = logging.getLogger(__name__)

# ==========================================================
# Structured Output Schema
# ==========================================================
# class ApplicationEmailSchema(BaseModel):
#     subject_line: str
#     body: str
#     HR_email_address: str

from pydantic import BaseModel
from typing import Optional

class EmailContent(BaseModel):
    subject_line: str
    body: str
    HR_email_address: str

class JobDetails(BaseModel):
    company_name: Optional[str]
    job_role: Optional[str]
    required_experience_years: Optional[str]

class ApplicationEmailSchema(BaseModel):
    application_email: EmailContent
    job_details: JobDetails


# ==========================================================
# Main Email Generator Class
# ==========================================================
class ApplicationEmailGenerator:

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def _make_llm_call(self, prompt: str, response_model, max_retries: int = 3) -> Optional[BaseModel]:
        for attempt in range(max_retries):
            try:
                response = self.client.responses.parse(
                    model="gpt-4o-mini",
                    input=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        {"role": "user", "content": prompt}
                    ],
                    text_format=response_model,
                )

                parsed = getattr(response, "output_parsed", None)
                if parsed is not None:
                    return parsed

                logger.warning(f"Retry {attempt + 1}/{max_retries}: empty or invalid LLM output")

            except Exception as e:
                logger.warning(f"Retry {attempt + 1}/{max_retries}: API error - {e}")

        logger.error("Failed to generate structured output after all retries")
        return None

    def generate_application_email(self, job_description: str):
        prompt = build_user_prompt(job_description)
        return self._make_llm_call(prompt, ApplicationEmailSchema)

# ==========================================================
# Script Entry Point
# ==========================================================
if __name__ == "__main__":
    # Load environment variables from .env
    load_dotenv()
    API_KEY = os.getenv("OPENAI_API")
    if not API_KEY:
        raise Exception("OPENAI_API_KEY missing in environment variables!")
    
    generator = ApplicationEmailGenerator(api_key=API_KEY)

    print("Paste the job description below (press Enter twice to finish):")
    job_description = """
📢 Hiring: hashtag#Python Developer & hashtag#AIML Developer | Surat, Gujarat

🔹 Job Role: hashtag#Python Developer
-Experience: 1+ Years
-Requirements: Strong Python skills, Django/Flask/FastAPI, REST APIs, and database handling.

🔹 Job Role: hashtag#AIML Developer
-Experience: Fresher – 1 Year
-Requirements: Good understanding of Python, machine learning concepts, and libraries like Pandas, NumPy, and Scikit-learn.

📍 Location: Surat, Gujarat

 📩 To Apply: Please share your resume at moxa@tekpillar.com
"""

    output = generator.generate_application_email(job_description)
    print("\nGenerated Application Email and Job Details:\n")
    print(output.model_dump())
    # if output:
    #     print("--------------------------------------------------")
    #     print("📌 Subject Line:")
    #     print(output.subject_line)
    #     print("\n📌 Body:")
    #     print(output.body)
    #     print("\n📌 HR Email:")
    #     print(output.HR_email_address)
    #     print("--------------------------------------------------")
    # else:
    #     print("Failed to generate application email.")
