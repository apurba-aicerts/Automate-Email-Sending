import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv


class EmailClient:
    def __init__(self, email_user: str, email_pass: str):
        if not email_user or not email_pass:
            raise ValueError("Email or password is missing!")

        self.email_user = email_user
        self.email_pass = email_pass
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, 
                   to_email: str, 
                   subject: str, 
                   body: str, 
                   file_path: str = r"Apurba_Manna_resume.pdf"):
        """
        Send an email using SMTP with optional file attachments.

        attachments: list of file paths
        """
        # Build the email message
        msg = MIMEMultipart()
        msg["From"] = self.email_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Attach files
        # if attachments:
        #     for file_path in attachments:
        if not os.path.isfile(file_path):
            print(f"⚠️ File not found: {file_path}")
            # continue

        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{os.path.basename(file_path)}"',
            )
            msg.attach(part)

        # SMTP flow
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_pass)
                server.send_message(msg)
            print("✅ Email sent successfully!")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")


if __name__ == "__main__":
    load_dotenv()
    EMAIL_USER = os.environ.get("EMAIL_USER")
    EMAIL_PASS = os.environ.get("EMAIL_PASS")

    client = EmailClient(EMAIL_USER, EMAIL_PASS)

    # Test email with attachment
    client.send_email(
        to_email="apurba_m@amsc.iitr.ac.in",
        subject="Automated Update with Attachment",
        body="Hello! Please find the attached document.",
        # attachments=["resume.pdf"]  # list your files here
    )
