import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app import models
from app.database import SessionLocal, engine
import logging
from app.tcp_server import run_tcp_server
import threading
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def start_tcp_server():
    logging.info("Starting TCP server thread")
    tcp_thread = threading.Thread(target=run_tcp_server)
    tcp_thread.daemon = True
    tcp_thread.start()

start_tcp_server()

if __name__ == "__main__":
    logging.info("Starting FastAPI server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
