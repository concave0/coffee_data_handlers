import requests 
from data_hanlders.organize import OrganizeData 
from mq_queue.sender_queue_mq import SenderClientRabbitMq
import datetime 

# Data class that stores, sends to queues, and holds the data coming from data collector.
class Data:
    
    organize_data = OrganizeData()

    # Get the data from the data collector get_data_wiki endpoint 
    def get_data(self) -> str :
        data = requests.get("http://0.0.0.0:8001/get_data_wiki", stream=True) 
        now  = datetime.datetime.now()
        path = f"data_hanlders/cache_data/{str(now)}_cache.json"
        with open(path, "wb") as file:
            for chunk in data.iter_content(chunk_size=8192): 
                file.write(chunk)
            file.close()
        return path 
    
    # Sending data to queue
    def send_data(self, id:int , queue :str, data:str , name:str , facts:str):
        sending = SenderClientRabbitMq()
        record = self.organize_data.set_details(id=id, name=name,facts=facts)
        sending.send_data(target_queue_name=queue, data=data)

    # Getting data from database
    def get_data_from_coffee_database(self,coffee_name:str) -> str: 
        return requests.get(f"http://0.0.0.0:8003/request_data/{coffee_name}").text 

        