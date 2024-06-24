import pika 
from mq_queue.queue_names import queues 
import json
import ast
import datetime
from database.database import  create_new_coffee


# Add middlewear to queue calls to your FastAPI routes  
class ConsumerClientRabbitMq: 

    data_recieved = {}
    requests_amount = 0

    def callback(self, ch, method, properties, body):
        # Recording data 
        now = str(datetime.datetime.now())
        str_body = ast.literal_eval(body.decode())
        for coffee_details , facts in str_body.items(): 
            create_new_coffee(id=facts[0] , name=coffee_details , facts=facts[1] , commit_date=now)
    
    # Listening for incoming messages from queue 
    def listen(self): 
        
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        for key, queue  in queues.__dict__.items(): 
            channel.queue_declare(queue=queue)
            channel.basic_consume(queue=queue, on_message_callback=self.callback, auto_ack=True)
            print(f"listening on {queue}")

        channel.start_consuming()

    # Create only one queue 
    def create_single_queue(self, queue_name:str): 
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.close()

    # Clean a single of the queue from the system (helps with system resources if there are to many)
    def clean_queue(self,queue_name:str): 
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        # Delete the queue
        channel.queue_delete(queue=queue_name)
        connection.close()

    def record_queue_list(self, key:int , q_name:str): 
        queues.__dict__[key] = q_name

    # Setting up queu at run time    
    def queue_setup(self,number_of_queues:int): 
        count = 0 
        while number_of_queues > 0: 
            queue = f'database{count}'
            self.create_single_queue(queue)
            self.record_queue_list(count, queue)

            number_of_queues -= 1 
            count += 1 
            
    # Clean all of the queue from the system (helps with system resources if there are to many)
    def tear_down_queues(self):
        for key, queue  in queues.__dict__.items(): 
            self.clean_queue(queue)

    # Saving quue data (response the the queue is receiving)
    def saved_data(self):
        # Save every 50 requests 
        if self.requests_amount == 50: 
            self.save_to_json(filename='database/mq_queue/tests_data/queue_responses.json',data=self.data_recieved)
            # Set back to 0 
            self.requests_amount = 0
    
    # Converting the data to json format
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




