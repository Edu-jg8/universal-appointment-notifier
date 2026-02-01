import csv
import logging
from datetime import datetime, timedelta

FORMATS = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]

logger = logging.getLogger(__name__)


# Function that detects the date format, returns the date as an object and its format
def parse_date(date_str):
    for fmt in FORMATS:
        try:
            date = datetime.strptime(date_str, fmt).date()
            return date, fmt
        except ValueError:
            pass
    return None, None


def get_appointments_to_notify(file_path):
    """
    Reads an appointments calendar from a CSV file and filters
    appointments that require notification today or tomorrow.

    Returns:
        list[dict]: A list of appointment dictionaries with an added
                    'reminder_type' field.
    """
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    to_notify = []

    try:
        with open(file_path, mode="r", encoding="utf-8-sig", newline="") as file:
            # Detect the separator automatically
            content = file.read(2048)
            file.seek(0)
            dialect = csv.Sniffer().sniff(content)

            # Detect and ignore empty lines at the begining
            pos = file.tell()
            line = file.readline()
            while line and not line.replace(dialect.delimiter, "").strip():
                pos = file.tell()
                line = file.readline()
            file.seek(pos)

            reader = csv.DictReader(file, dialect=dialect)

            for line_num, row in enumerate(reader, start=2):

                # Exiting the loop if we dont have information(more eficientcy)
                if not any(row.values()):
                    continue

                # Header normalization (clean-code personal branding)
                clean_row = {k.strip().casefold(): v for k, v in row.items() if k}

                # Exiting the loop if we do have information but not the date
                date_str = clean_row.get("date", "").strip()
                if not date_str:
                    logger.info(f"non-existent date in line {line_num}")
                    continue

                try:
                    apt_date, format = parse_date(date_str)
                    logger.info(f"Date calculated using {format} format")
                    if not apt_date:
                        logger.warning(
                            f"Line {line_num}: Invalid date '{date_str}'. Expected ISO format YYYY/MM/DD or European format DD/MM/YYYY."
                        )
                        continue
                except (ValueError, OverflowError):
                    logger.warning(
                        f"Line {line_num}: Invalid date '{date_str}'. Expected ISO format YYYY/MM/DD or European format DD/MM/YYYY."
                    )
                    continue

                # CORE BUSINESS LOGIC:
                # - Tomorrow → Preventive reminder
                # - Today → Same-day appointment notification
                if apt_date == tomorrow:
                    clean_row["reminder_type"] = "REMINDER: Appointment scheduled for tomorrow"
                    to_notify.append(clean_row)

                elif apt_date == today:
                    clean_row["reminder_type"] = "NOTICE: Appointment scheduled for today"
                    to_notify.append(clean_row)

        return to_notify

    except FileNotFoundError:
        logger.error(f"Appointments file not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred while processing CSV in line{line_num}:{e}")
        return None
