import pika

class RabbitMQService:
    def __init__(self, queue='events'):
        self.queue = queue
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def publish(self, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=message.encode()
        )

    def consume(self, callback):
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=callback,
            auto_ack=True
        )
        self.channel.start_consuming()
