import smtplib
import os
import logging
import time
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables (security configuration)
load_dotenv()
logger = logging.getLogger(__name__)


def load_template(template_path):
    """
    Loads an email template from disk.

    Args:
        template_path (str): Path to the template file.

    Returns:
        str: The raw template content. If the file is missing, returns
             a safe fallback template.
    """
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.warning(f"Could not read template ({e}). Using hardcoded fallback.")
        # Fallback template to avoid breaking the notification flow
        return "Appointment reminder: {service} on {date} at {time}."


def send_appointment_notifications(appointments, template_path):
    """
    Connects to an SMTP server and sends personalized appointment notifications.

    Args:
        appointments (list[dict]): List of appointment dictionaries. Each dict
            should include at least: 'email', 'client_name', 'service', 'date',
            'time', 'location', and 'reminder_type'.
        template_path (str): Path to the email template file.

    Returns:
        None
    """
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not user or not password:
        logger.error("Email credentials are not configured in the .env file.")
        return

    raw_template = load_template(template_path)

    try:
        # High-security encrypted connection (SSL)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(user, password)

            for apt in appointments:
                # Recipient email is taken directly from the appointment dictionary
                recipient = apt.get("email", "").strip()

                if not recipient:
                    logger.warning(
                        f"Skipping appointment for '{apt.get('client_name', 'Unknown')}': Missing email address."
                    )
                    continue

                msg = EmailMessage()
                # Subject contains the reminder type, enabling quick filtering in inboxes
                msg["Subject"] = f"🔔 {apt.get('reminder_type', 'Appointment Reminder')}"
                msg["From"] = user
                msg["To"] = recipient

                try:
                    # Professional data injection into the email template
                    body = raw_template.format(
                        name=apt.get("client_name", "Client"),
                        service=apt.get("service", "Service"),
                        date=apt.get("date", "N/A"),
                        time=apt.get("time", "N/A"),
                        location=apt.get("location", "Our office"),
                    )

                    msg.set_content(body)
                    server.send_message(msg)
                    logger.info(f"Reminder successfully sent to: {recipient}")
                    time.sleep(1.5)  # to avoid spam blocks

                except KeyError as e:
                    # Template contains a placeholder not provided in .format(...)
                    logger.error(f"Template error: Missing placeholder {e} without spaces and in lowercase")
                    continue

    except smtplib.SMTPAuthenticationError as e:
        logger.error("SMTP Login Failed: Check your credentials or App Password.")

    except Exception as e:
        logger.error(f"Critical SMTP connection failure: {e}")
