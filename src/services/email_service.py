import smtplib
from email.message import EmailMessage
from src.config.settings import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    ALERT_EMAIL_TO,
)
import os


class EmailService:
    def __init__(self):
        self.smtp_host = SMTP_HOST
        self.smtp_port = SMTP_PORT
        self.smtp_user = SMTP_USER
        self.smtp_password = SMTP_PASSWORD
        self.to_email = ALERT_EMAIL_TO
    def send_violation_alert(
        self,
        title: str,
        body: str,
        snapshot_path: str | None = None,
    ):
        msg = EmailMessage()
        msg["Subject"] = title
        msg["From"] = self.smtp_user
        msg["To"] = self.to_email
        msg.set_content(body)

        # Attach snapshot if exists
        if snapshot_path and os.path.exists(snapshot_path):
            with open(snapshot_path, "rb") as f:
                img_data = f.read()
            msg.add_attachment(
                img_data,
                maintype="image",
                subtype="jpeg",
                filename=os.path.basename(snapshot_path),
            )

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
        except Exception as e:
            print(f"[EmailService] Failed to send email: {e}")
