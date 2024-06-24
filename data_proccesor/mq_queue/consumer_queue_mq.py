import pika 
from mq_queue.queue_names import queues 
import json
import datetime

# Add middlewear to queue calls to your FastAPI routes  
class ConsumerClientRabbitMq: 

    data_recieved = {}
    requests_amount = 0

    # Takes he data in and then saves it
    def callback(self, ch, method, properties, body):
        # Recording data 
        now = str(datetime.datetime.now())
        str_body = str(body)
        self.data_recieved[now] = str_body
        self.saved_data()
        self.requests_amount += 1 
        print(f" [x] Received {body}")

    # Listens for incoming data in coming from the Rabbit MQ
    def listen(self): 
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        for key, queue  in queues.__dict__.items(): 
            channel.queue_declare(queue=queue)
            channel.basic_consume(queue=queue, on_message_callback=self.callback, auto_ack=True)
            print(f"listening on {queue}")
        channel.start_consuming()

    # Create a single queue 
    def create_single_queue(self, queue_name:str): 
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.close()

    # Create a clean a single queue
    def clean_queue(self,queue_name:str): 
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        # Delete the queue
        channel.queue_delete(queue=queue_name)
        connection.close()

    # Record the names of each queue so that it can be referenced later
    def record_queue_list(self, key:int , q_name:str): 
        queues.__dict__[key] = q_name
    
    # Set up each queue
    def queue_setup(self,number_of_queues:int): 
        count = 0 
        while number_of_queues > 0: 
            queue = f'data_proccesor{count}'
            self.create_single_queue(queue)
            self.record_queue_list(count, queue)
            number_of_queues -= 1 
            count += 1 
            
    # Tear down each queue  (helps with system resources)
    def tear_down_queues(self):
        for key, queue  in queues.__dict__.items(): 
            self.clean_queue(queue)

    # Save data
    def saved_data(self):
        # Save every 50 requests 
        if self.requests_amount == 50: 
            self.save_to_json(filename='database/mq_queue/tests_data/queue_responses.json',data=self.data_recieved)
            # Set back to 0 
            self.requests_amount = 0
            
    # Save data and then convert it to json       
    def save_to_json(self, data, filename, indent=4):

        try:
            existing_data = {}
            with open(filename, 'r') as f:
                try:
                    existing_data = json.load(f)

                except json.JSONDecodeError:
                    pass

            existing_data.update(data)  
            
            with open(filename, 'w') as f:
                json.dump(existing_data, f, indent=indent)
                f.close()
                print(f"Data updated successfully in '{filename}'.")

        except IOError as e:
                print(f"Error updating data: {e}")




