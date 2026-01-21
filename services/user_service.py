import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from messaging import RabbitMQService

def callback(ch, method, properties, body):
    print(f"📊 Evento registrado: {body.decode()}")

rabbit = RabbitMQService()
print("👤 Serviço de Usuário aguardando eventos...")
rabbit.consume(callback)
