import unittest
import datetime 
import random 
import json 

from database.database import get_all_coffee , get_specfic_coffee_details , create_new_coffee  , CoffeeData
from health_check.test_health_check import HealthCheck 

class AppilcationUnitTests(unittest.TestCase): 


    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName) 
        self.details = self.set_details()

    # Helper function
    def generate_random_number(self):
        start=0
        end=100000000000
        return random.randint(start, end - 1)

    # Setting details to be given the database
    def set_details(self) -> list[int]: 
        id = self.generate_random_number()
        name = self.generate_random_number()
        facts = self.generate_random_number()
        return [id, name , facts]
    
    # Database tests 
    def test_create_new_coffee(self): 
        id = self.details[0]
        name = self.details[1]
        facts = self.details[2]
        now = str(datetime.datetime.now())
        creating_coffee_details = create_new_coffee(id=id , name=name, facts=facts, commit_date=now)
        self.assertTrue(creating_coffee_details[1] == True)

    # Performing Health Check on the database endpoints
    def test_checking_routes_get_data(self):
        health = HealthCheck() 
        status_code = health.checking_routes_get_data()
        self.assertTrue(status_code == 200)
    
    # Preforming health check on the metrics endpoints
    def test_health_mertrics(self): 
        health = HealthCheck() 
        status_code = health.checking_routes_metrics()
        self.assertTrue(status_code == 200)


if __name__ == '__main__':
    unittest.main()
