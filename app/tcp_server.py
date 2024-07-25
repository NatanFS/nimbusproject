import logging
from twisted.internet import reactor, protocol
from sqlalchemy.orm import sessionmaker
from .database import engine
from app import crud_client
from .schemas import ClientCreate

SessionLocal = sessionmaker(bind=engine)

class DataReceiver(protocol.Protocol):
    def connectionMade(self):
        logging.info(f"Connection established with {self.transport.getPeer()}")

    def dataReceived(self, data):
        message = data.decode('utf-8')
        logging.info(f"Data received: {message}")
        parts = message.split(',')

        if len(parts) == 4:
            name, email, phone, age = parts
            try:
                age = int(age)
                db = SessionLocal()
                client_data = ClientCreate(name=name, email=email, phone=phone, age=age)
                crud_client.create_client(db, client_data)
                self.transport.write(b"Ok")
                db.close()
                logging.info(f"Received and stored data: {name}, {email}, {phone}, {age}")
            except Exception as e:
                self.transport.write(b"Erro ao adicionar cliente")
                logging.error(f"Error storing data: {e}")
        else:
            self.transport.write(b"Error")
            logging.error("Received data in incorrect format")

class DataReceiverFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return DataReceiver()

def run_tcp_server():
    port = 5784
    logging.info(f"Starting TCP server on port {port}")
    reactor.listenTCP(port, DataReceiverFactory())
    reactor.run()
