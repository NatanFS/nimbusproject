import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import argparse
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from app.database import Base
from app import crud_client
from app.report_generator import generate_report_pdf
from app.email_utils import send_email
from app.utils import format_date
import csv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

logging.basicConfig(filename='report.log', level=logging.INFO)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate and send meteorological reports.")
    parser.add_argument('--phones', required=True, help="Phone numbers, separated by commas.")
    parser.add_argument('--date', required=True, help="Date in the format YYYY-MM-DDTHH:MM.")
    parser.add_argument('--send_email', action='store_true', help="Flag to send the report by email.")
    parser.add_argument('--raw', required=True, help="Path to the raw report file.")
    return parser.parse_args()

def process_json_or_txt_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def process_csv_file(file_path):
    data = {"análise": [], "previsao": []}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            section = row.pop('section')
            if section in data:
                data[section].append(row)
    return data

def process_raw_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension in ['.json', '.txt']:
        return process_json_or_txt_file(file_path)
    elif file_extension == '.csv':
        return process_csv_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def main():
    args = parse_arguments()
    logging.info(f"Received parameters: {args}")

    try:
        phone_list = args.phones.split(',')
        db = SessionLocal()
        client_data = crud_client.get_clients_by_phones(db, phone_list)
        if not client_data:
            logging.error("No client data found for the provided phone numbers.")
            return
        
        for client in client_data:
            client_name = client.name
            report_date = args.date
            report_date = format_date(report_date)
            data = process_raw_file(args.raw)
            logging.info("Raw file processed successfully.")
            
            pdf_buffer = generate_report_pdf(data, client_name, report_date)
            logging.info(f"Report PDF generated successfully for {client_name}.")
            
            if args.send_email:
                send_email(pdf_buffer, [client.email], report_date)
    except Exception as e:
        logging.error(f"Error during script execution: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
