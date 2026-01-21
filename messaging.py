import pika
import uuid
import json

# Configuração Padrão do RabbitMQ (Local)
RABBITMQ_HOST = 'localhost'


class RabbitMQClient:
    """
    Usado pelo Gateway para enviar requisições aos serviços.
    Implementa o padrão RPC (Remote Procedure Call).
    """

    def __init__(self):
        # Conecta ao broker
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()

        # Cria uma fila temporária exclusiva para receber as respostas
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        # Diz ao RabbitMQ para enviar respostas dessa fila para a função on_response
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        # Verifica se a resposta recebida corresponde à pergunta feita (correlation_id)
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, service_queue, data):
        """
        Envia a mensagem para um serviço específico e espera a resposta.
        :param service_queue: Nome da fila do serviço (ex: 'catalogo_queue')
        :param data: Dicionário com os dados da requisição
        """
        self.response = None
        self.corr_id = str(uuid.uuid4())  # ID único da requisição

        # Publica a mensagem na fila do serviço
        self.channel.basic_publish(
            exchange='',
            routing_key=service_queue,  # Para quem vai a mensagem
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,  # Onde quero receber a resposta
                correlation_id=self.corr_id,  # ID para rastrear o pedido
            ),
            body=json.dumps(data))  # Converte dados para JSON

        # Loop que bloqueia e espera até a resposta chegar
        while self.response is None:
            self.connection.process_data_events()

        return self.response


class RabbitMQService:
    """
    Usado pelos Serviços (Catálogo, Playlist) para receber pedidos.
    """

    def __init__(self, service_queue, business_logic_callback):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.queue_name = service_queue
        self.business_logic = business_logic_callback  # Função que processa os dados

        # Cria a fila do serviço se não existir
        self.channel.queue_declare(queue=self.queue_name)

        # Configura o consumo de mensagens
        self.channel.basic_qos(prefetch_count=1)  # Não sobrecarrega o worker
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_request)

        print(f" [*] Serviço '{self.queue_name}' aguardando requisições...")

    def on_request(self, ch, method, props, body):
        request_data = json.loads(body)
        print(f" [x] Recebido: {request_data}")

        # --- Executa a lógica do serviço real ---
        response_data = self.business_logic(request_data)
        # ----------------------------------------

        # Envia a resposta de volta para a fila temporária do Gateway
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=json.dumps(response_data))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        self.channel.start_consuming()