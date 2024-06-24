from data_hanlders.data_hanlders_process import HandleProccesing
from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Thread
from apscheduler.triggers.interval import IntervalTrigger

# Cron jobs for updating the database
class UpdateDatabaseWorkers: 
    
    def __init__(self) -> None:
        self.scheduler = BlockingScheduler()

    # Defining the jobs that need to be set
    def workers_store_data(self): 
        handling_data = HandleProccesing()
        handling_data.store_data()

    # Setting the jobs and setting a interval the run them at
    def set_jobs(self): 
        trigger = IntervalTrigger(seconds=10)
        self.scheduler.add_job(self.workers_store_data, trigger)
    
    # Starting jobs and then starting the scheduler thread
    def start_scheduler(self):
        scheduler_thread = Thread(target=self.scheduler.start)
        scheduler_thread.start()
        print("Updating Dtabase thread started")