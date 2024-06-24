import requests 

# TODO NOTE THERE IS SOMETHING WRONG THESE TEST! THERE IS NOTHING WRONG WITH YOUR APPILCATION

# Defining the target endpoints for health \
class HealthCheck:     

    def __init__(self) -> None:
        pass 
    
    # Checking the giving ids endpoint
    def check_give_ids(self) -> int: 
        url = "http://0.0.0.0:8006/give_ids"
        status_code = requests.get(url=url).status_code
        return status_code
    
    # Checking the metrics endpont that prometheus collects from
    def check_metrics(self) -> int: 
        url = "http://0.0.0.0:8006/metrics"
        status_code = requests.get(url=url).status_code
        return status_code


class HealthCheckTest(): 

    def health_check_give_ids(self): 
        health_check  = HealthCheck()
        status_code = health_check.check_give_ids()
        print(f"status code for health check give_ids is currently {status_code}")
        assert(status_code==200)

    def health_check_metrics(self): 
        health_check  = HealthCheck()
        status_code = health_check.check_metrics()
        print(f"status code for health check metrics is currently {status_code}")
        assert(status_code==200)

