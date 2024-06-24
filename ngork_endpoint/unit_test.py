import unittest
import requests 
import json
import os 
import jwt 
from give_token import TokenInTransit 

class UnitTest(unittest.TestCase): # NOTE appilcation must be running for this
    
    def is_json(self, data):
        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False

    def generate_jwt(self):
        payload = {"application": "test", "exp": 999999999999999999999999999}  # random long number
        api_token = self.load_env_var()
        token = jwt.encode(payload, api_token, algorithm="HS256")  
        return token

    def load_env_var(self) -> str: 
        api_key = os.environ.get("API_KEY")  
        if api_key:
            return api_key
        else:
            return "API_KEY not set"

    # Testing routing of that gets the coffee ids
    def test_check_redirected_service_ids(self): 
        headers = {"Authorization": f"Bearer {self.generate_jwt()}"}
        url = "http://0.0.0.0:8080/ngork_endpoint/id"
        data = requests.get(url,headers=headers)
        is_valid_data = self.is_json(data.text)
        self.assertTrue(is_valid_data==True and data.status_code == 200)

    # Testing the routing that gets the data from the database
    def test_check_redirected_database(self): 
        specfic_coffee_id = "1274978100"
        url= f"http://0.0.0.0:8080/ngork_endpoint/data"
        headers = {
            "Authorization": f"Bearer {self.generate_jwt()}",
            "User-Agent": "MyCustomClient",
            "Accept": "application/json",
            "X-Request-ID": f"{specfic_coffee_id}"
            }
        data = requests.get(url, headers=headers)
        is_valid_data = self.is_json(data.text)
        self.assertTrue(is_valid_data==True and data.status_code == 200)
    
    # Testing and simulating what it would be for the website to give its Token
    def test_recieve_token(self): 
        api_token = self.load_env_var()
        transit = TokenInTransit()
        url = "http://0.0.0.0:8080/updating_api_key"
        token_give = transit.give(token=api_token,endpoint=url)
        self.assertTrue(token_give.status_code == 200)

if __name__ == '__main__':
    unittest.main()
