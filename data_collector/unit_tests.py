import unittest
import os 
from threading import Thread 
from collector.data_collector import CollectDataFromSearch 
from search.search_apis import SearchWiki
import requests 
import json 

class AppilcationUnitTests(unittest.TestCase): 
    
    def testing_batch_job_collect(self): 
        self.assertTrue(os.path.getsize("raw_data/raw_data.json") !=  0)  # If the size of the not 0 then it recording okay. 

    def testing_data_quality(self): 
        bugs = "bugs/bugs.txt"
        self.assertTrue(os.path.getsize(bugs) ==  0) # If there are no bugs being recorded during data collection then the data is good. 

    def testing_health__status(self): 
        app_health_data = "metrics/health_check_data/api_health.json"
        length = os.path.getsize(app_health_data)
        self.assertTrue(os.path.getsize(app_health_data) == 8) # If file is no more then the default length of 8 in this file then the each endpoint is responding with a 200 code and is fine. That is being collected by test_health_check.py 
    
    def testing_prometheus_status(self):
        respose = requests.get("http://localhost:9090/") # check if it is up
        self.assertTrue(respose.status_code==200)
    
    def testing_is_up(self): 
        response = requests.get("http://0.0.0.0:8001/") # appilcation is running
        self.assertTrue(response.status_code==200)

    def testing_get_wiki_data(self): 
        response = requests.get("http://0.0.0.0:8001/get_data_wiki")
        self.assertTrue(response.status_code==200)

    def testing_metrics(self): 
        response = requests.get("http://0.0.0.0:8001/metrics")
        self.assertTrue(response.status_code==200)

    
if __name__ == '__main__':
    unittest.main()


        



