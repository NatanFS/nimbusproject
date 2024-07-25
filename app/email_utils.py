import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os
import logging

load_dotenv()

def send_email(pdf_buffer, recipients, report_date_str):
    from_email = os.getenv('EMAIL_HOST_USER')
    password = os.getenv('EMAIL_HOST_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = f"Meteorological Report - {report_date_str}"
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf_buffer.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="report.pdf"')
    msg.attach(part)
    
    try:
        SMTP_HOST = os.getenv('SMTP_EMAIL_HOST')
        with smtplib.SMTP(SMTP_HOST, 587) as smtp:
            smtp.starttls()
            smtp.login(from_email, password)
            smtp.sendmail(from_email, recipients, msg.as_string())
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
