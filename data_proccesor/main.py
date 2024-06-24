from threading import Thread 

from mq_queue.consumer_queue_mq import ConsumerClientRabbitMq 
from workers.UpdateDatabaseWorkers import UpdateDatabaseWorkers

from routes.routes import router 

from fastapi import FastAPI
import uvicorn
from mq_queue.consumer_queue_mq import ConsumerClientRabbitMq 
from prometheus_fastapi_instrumentator import Instrumentator

# Config for server
app =  FastAPI()
app.include_router(router)

# Prometheus metrics middleware config 
instrumentator = Instrumentator().instrument(app).expose(app , include_in_schema=False)
instrumentator.should_group_status_codes = True 
instrumentator.should_exclude_streaming_duration = True
instrumentator.should_instrument_requests_inprogress = True 

def run_queue():
    mq_queue = ConsumerClientRabbitMq()
    mq_queue.queue_setup(2)
    mq_queue.listen()

def run_updating_database(): 
    update_database = UpdateDatabaseWorkers()
    update_database.set_jobs()
    update_database.start_scheduler()

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8006)
    
if __name__ == "__main__": 

    queue_thread = Thread(target=run_queue)
    updating_database_thread = Thread(target=run_updating_database)
    server_thread = Thread(target=run_server) 

    queue_thread.start()
    updating_database_thread.start()
    server_thread.start()

    queue_thread.join()
    updating_database_thread.join()
    server_thread.join()
