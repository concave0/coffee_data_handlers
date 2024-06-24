import requests 
import json 

# Testing each endpoint to see if it is up and running. 
class HealthCheck: 

    def __init__(self) -> None: 
        self.coffee_id = self.find_id('Coffee')
        
        self.routes = {
            "get_data" :  f"http://0.0.0.0:8003/request_data/{self.coffee_id}", 
            "get_metrics": f"http://0.0.0.0:8003/metrics",
        }

    def find_id(self, target_id:str): 
        with open("routes/ids_data/ids.json", "r") as file: 
            data = json.loads(json.dumps(json.load(file)))
        file.close()
        return data.get(target_id)
    
    def checking_routes_get_data(self) -> int: 
        data = self.routes.get("get_data")
        status_code  = requests.get(data).status_code
        return status_code
    
    def checking_routes_metrics(self) -> int: 
        data = self.routes.get("get_metrics")
        status_code  = requests.get(data).status_code
        return status_code
        