# import os
# from dotenv import load_dotenv
# from application_email_generator import ApplicationEmailGenerator
# from email_client import EmailClient


# # ---------------------------------------------------------
# # Paste Your JD Here (or load from a file)
# # ---------------------------------------------------------
# JOB_DESCRIPTION = """
# 📢 Hiring: #Python Developer & #AIML Developer | Surat, Gujarat

# 🔹 Job Role: Python Developer
# - Experience: 1+ Years
# - Requirements: Python, Django/Flask/FastAPI, REST APIs, Databases

# 🔹 Job Role: AIML Developer
# - Experience: Fresher – 1 Year
# - Requirements: Python, ML, Pandas, NumPy, Scikit-learn

# 📍 Location: Surat, Gujarat
# 📩 To Apply: Please share your resume at apurba_m@amsc.iitr.ac.in
# """


# def main():

#     # Load environment variables
#     load_dotenv()

#     OPENAI_API = os.getenv("OPENAI_API")
#     EMAIL_USER = os.getenv("EMAIL_USER")
#     EMAIL_PASS = os.getenv("EMAIL_PASS")

#     if not OPENAI_API:
#         raise Exception("Missing OPENAI_API in .env file")
#     if not EMAIL_USER or not EMAIL_PASS:
#         raise Exception("Missing EMAIL_USER or EMAIL_PASS in .env file")

#     # Initialize LLM generator + email sender
#     generator = ApplicationEmailGenerator(api_key=OPENAI_API)
#     mailer = EmailClient(email_user=EMAIL_USER, email_pass=EMAIL_PASS)

#     # Generate email from LLM
#     print("🔄 Generating HR-ready email...")
#     output = generator.generate_application_email(JOB_DESCRIPTION)

#     if not output:
#         print("❌ LLM generation failed")
#         return

#     subject = output.subject_line
#     body = output.body
#     hr_email = output.HR_email_address

#     print("\n----------------------------------------------")
#     print("📌 Subject:", subject)
#     print("📌 HR Email:", hr_email)
#     print("📌 Body:\n", body)
#     print("----------------------------------------------\n")

#     # Auto-send email (no confirmation)
#     print("📤 Sending email to HR automatically...")
#     mailer.send_email(to_email=hr_email, subject=subject, body=body)

#     print("✅ Done!")


# if __name__ == "__main__":
#     main()
