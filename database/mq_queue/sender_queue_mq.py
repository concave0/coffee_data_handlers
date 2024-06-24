import pika 

# Rabbit MQ client 
class SenderClientRabbitMq: 
    def send_data(self, target_queue_name:str, data: None):
        connection = pika.BlockingConnection( pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=target_queue_name)
        channel.basic_publish(exchange='', routing_key=target_queue_name, body=data)
        connection.close()

