import logging.config
import yaml
from fastapi import FastAPI
from app import models
from app.database import SessionLocal, engine
from app.tcp_server import run_tcp_server
import threading
from contextlib import asynccontextmanager

with open('logging_tcp.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger('app')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def start_tcp_server():
    logger.info("Starting TCP server thread")
    run_tcp_server()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    tcp_thread = threading.Thread(target=start_tcp_server)
    tcp_thread.daemon = True
    tcp_thread.start()
    
    yield

    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="info")
