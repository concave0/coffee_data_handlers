# Check health of endpoints if you get a anything a 200 code 
import requests 
import json 
import datetime


class HealthCheck: 
    def __init__(self) -> None:
       
        self.routes = {
            "wiki_data" : "http://0.0.0.0:8001/get_data_wiki",
        }

    # Save data to JSON
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
                print(f"Data updated successfully in '{filename}'.")
        except IOError as e:
                print(f"Error updating data: {e}")

    # Calling routes to make sure they are up and running
    def checking_routes(self): 
        for name, route in self.routes.items():
            try: 
                status = requests.get(route).status_code
                assert status == 200 
                print(f"{route} is fine.")
            except AssertionError as e: 
                error = f"The error for route {route} is {e} and the status code was {status}"
                now  = str(datetime.datetime.now())
                data = { now : error}
                self.save_to_json(data = data, filename="data_collector/metrics/health_check_data/api_health.json")

