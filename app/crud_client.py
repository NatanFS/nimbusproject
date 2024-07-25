import logging
from sqlalchemy.orm import Session
from app import models, schemas

def get_client_by_phone(db: Session, phone: str):
    logging.info(f"Fetching client with phone: {phone}")
    return db.query(models.Client).filter(models.Client.phone == phone).first()

def get_clients_by_phones(db: Session, phones: list):
    logging.info(f"Fetching clients with phones: {phones}")
    return db.query(models.Client).filter(models.Client.phone.in_(phones)).all()

def create_client(db: Session, client: schemas.ClientCreate):
    logging.info(f"Creating client: {client}")
    db_client = models.Client(name=client.name, email=client.email, phone=client.phone, age=client.age)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    logging.info(f"Client created with ID: {db_client.id}")
    return db_client
