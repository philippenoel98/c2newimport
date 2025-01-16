# logging_module.py
import logging
from logging.handlers import RotatingFileHandler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("app.log", maxBytes=5 * 1024 * 1024, backupCount=3),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def generate_report():
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    report_file = f"report_{current_datetime}.txt"
    
    try:
        with open(report_file, "w") as file:
            file.write("Log Report\n")
            file.write("=" * 40 + "\n")
            with open("app.log", "r") as log_file:
                file.write(log_file.read())
        logger.info("Report successfully generated: %s", report_file)
        return report_file
    except Exception as e:
        logger.error("Failed to generate report: %s", str(e))
        return None

def send_email(report_file):

    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = "pnoel@csdulittoral.qc.ca"
        msg['To'] = "pnoel@csdulittoral.qc.ca"
        msg['Subject'] = "Log Report"

        # Add body
        body = "Please find the attached log report."
        msg.attach(MIMEText(body, 'plain'))

        # Attach the file
        with open(report_file, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={report_file}',
            )
            msg.attach(part)

        # Send the email
        with smtplib.SMTP("smtp.office365.com", "587") as server:
            server.starttls()
            server.login("pnoel@csdulittoral.qc.ca", "Beatsbydrdre1!")
            server.sendmail("pnoel@csdulittoral.qc.ca", "pnoel@csdulittoral.qc.ca", msg.as_string())
        logger.info("Email sent successfully to %s", "pnoel@csdulittoral.qc.ca")
    except Exception as e:
        logger.error("Failed to send email: %s", str(e))
