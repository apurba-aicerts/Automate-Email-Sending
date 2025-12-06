import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv


class EmailClient:
    def __init__(self, email_user: str, email_pass: str):
        if not email_user or not email_pass:
            raise ValueError("Email or password is missing!")

        self.email_user = email_user
        self.email_pass = email_pass
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, to_email: str, subject: str, body: str):
        """Send an email using SMTP with TLS."""

        # Build the email message
        msg = MIMEMultipart()
        msg["From"] = self.email_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # SMTP flow
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_pass)
                server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    EMAIL_USER = os.environ.get("EMAIL_USER")
    EMAIL_PASS = os.environ.get("EMAIL_PASS")

    # Initialize client
    client = EmailClient(EMAIL_USER, EMAIL_PASS)

    # Test email
    client.send_email(
        to_email="apurba_m@amsc.iitr.ac.in",
        subject="Automated Update",
        body="Hello from Python automation using class!"
    )