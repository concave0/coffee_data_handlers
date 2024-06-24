import pika 

# Rabbit MQ Client
class SenderClientRabbitMq: 
    def send_data(self, target_queue_name:str, data):
        connection = pika.BlockingConnection( pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        tunnel = channel.queue_declare(queue=target_queue_name)
        channel.basic_publish(exchange='', routing_key=target_queue_name, body=str(data))
        connection.close()
        return tunnel 


