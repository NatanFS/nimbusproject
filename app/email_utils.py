import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os
import logging

load_dotenv()

def send_email(pdf_path, recipients, report_date):
    from_email = os.getenv('EMAIL_HOST_USER')
    password = os.getenv('EMAIL_HOST_PASSWORD')
    smtp_host = os.getenv('SMTP_EMAIL_HOST')
    smtp_port = int(os.getenv('SMTP_EMAIL_PORT', 587))

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = f"Relatório Meteorológico - {report_date}"

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(pdf_path, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(pdf_path)}"')
    msg.attach(part)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.ehlo() 
            smtp.starttls()
            smtp.ehlo()
            smtp.login(from_email, password)
            smtp.sendmail(from_email, recipients, msg.as_string())
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
