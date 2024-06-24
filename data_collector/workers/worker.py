from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from collector.data_collector import CollectDataFromSearch 
from health_check.test_health_check import HealthCheck

# Calling collector search that calls search apis to schedule batch Jobs
class Worker(): 

    def __init__(self) -> None:
         self.scheduler = BlockingScheduler() 

    def search_wiki(self): 
        search = CollectDataFromSearch()
        search.settings()
        search.batch_job_collect()

    def health_check(self): 
        health_check = HealthCheck()
        health_check.checking_routes()

    def set_jobs(self): 
        print("Worker thread started")
        trigger = IntervalTrigger(seconds=86400) # Record user input every 24 hours
        self.scheduler.add_job(self.search_wiki, trigger)
        self.scheduler.add_job(self.health_check, trigger)


        


