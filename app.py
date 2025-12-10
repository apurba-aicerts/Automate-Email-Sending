import os
import streamlit as st
from dotenv import load_dotenv
from application_email_generator import ApplicationEmailGenerator
from email_client import EmailClient
from db import JobStorage
# Load environment variables
load_dotenv()
OPENAI_API = os.getenv("OPENAI_API")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

if not OPENAI_API or not EMAIL_USER or not EMAIL_PASS:
    st.error("Missing environment variables: OPENAI_API, EMAIL_USER, EMAIL_PASS")
    st.stop()

# Initialize LLM and Email client
generator = ApplicationEmailGenerator(api_key=OPENAI_API)
mailer = EmailClient(email_user=EMAIL_USER, email_pass=EMAIL_PASS)
storage = JobStorage()
# -------------------------
# UI
# -------------------------
st.title("📩 Send HR-Ready Job Application Email")
st.markdown("Click the button below to generate and send email to HR automatically.")

# Optional: pre-fill Job Description
JOB_DESCRIPTION = """
📢 Hiring: #Python Developer & #AIML Developer | Surat, Gujarat
📩 To Apply: Please share your resume at apurba_m@amsc.iitr.ac.in
"""

st.text_area("Job Description (editable)", value=JOB_DESCRIPTION, height=150, key="jd")

if st.button("📤 Send Email to HR"):
    job_description = st.session_state.jd.strip()
    if not job_description:
        st.warning("Please enter a job description!")
    else:
        with st.spinner("Generating and sending email..."):
            # Generate email
            output = generator.generate_application_email(job_description)
            print(output)
            if not output:
                st.error("❌ Failed to generate email from LLM")
            else:
                # check on db
                if not storage.get_job(output.application_email.HR_email_address):
                    storage.save_job(
                        company_name=output.job_details.company_name,
                        job_role=output.job_details.job_role,
                        experience_required=output.job_details.required_experience_years,
                        job_description=job_description,
                        hr_email=output.application_email.HR_email_address
                    )
                    try:
                        # Send email
                        mailer.send_email(
                            to_email=output.application_email.HR_email_address,
                            subject=output.application_email.subject_line,
                            body=output.application_email.body
                        )
                        st.success(f"✅ Email sent to HR ({output.application_email.HR_email_address}) successfully!")
                    except Exception as e:
                        st.error(f"❌ Failed to send email: {e}")
                else:
                    st.info("ℹ️ Email to this HR address has already been sent and stored in the database.")
