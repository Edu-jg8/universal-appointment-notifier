import logging
import os
from src.logic import get_appointments_to_notify
from src.email_engine import send_appointment_notifications

# 1.LOGGER CONFIGURATION
# Logs are written to 'logs/activity.log' and also displayed in the console.
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("logs/activity.log", mode="w", encoding="utf-8"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def check_environment():
    """
    Validates that all critical files exist before starting the application.

    Returns:
        bool: True if all required files are present, False otherwise.
    """
    critical_files = [".env", "data/appointments.csv", "templates/appointment_reminder.txt"]

    for file in critical_files:
        if not os.path.exists(file):
            logger.error(f"FATAL: Required file not found: {file}")
            return False

    return True


def main():
    logger.info("--- Starting Universal Appointment Notifier ---")

    # 2. ENVIRONMENT INTEGRITY VALIDATION
    if not check_environment():
        logger.warning("System startup aborted. Please check missing files.")
        return

    # 3. PATH DEFINITIONS (os.path used for maximum cross-platform compatibility)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PATH_CSV = os.path.join(BASE_DIR, "data", "appointments.csv")
    PATH_TEMPLATE = os.path.join(BASE_DIR, "templates", "appointment_reminder.txt")

    # 4. PHASE 1: DATA PROCESSING (Business Logic)
    logger.info("Analyzing appointments database...")
    appointments = get_appointments_to_notify(PATH_CSV)

    if appointments is None:
        # Error already logged inside logic.py (e.g., FileNotFoundError)
        return

    if not appointments:
        logger.info("No appointments found that require notification today.")
        return

    # 5. PHASE 2: NOTIFICATION DELIVERY (Email Engine)
    logger.info(f"{len(appointments)} appointment(s) pending notification.")
    send_appointment_notifications(appointments, PATH_TEMPLATE)

    logger.info("--- Process completed ---")


if __name__ == "__main__":
    main()
