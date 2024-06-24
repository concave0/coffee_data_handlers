from threading import Thread 
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.gzip import GZipMiddleware
from routes.routes import router  
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

#  Add GZip middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8003)

def run_queue():
    mq_queue = ConsumerClientRabbitMq()
    mq_queue.queue_setup(2)
    mq_queue.listen()

if __name__ == "__main__": 

    server_thread = Thread(target=run_server) 
    queue_thread = Thread(target=run_queue)
  
    server_thread.start()
    queue_thread.start()
  
    server_thread.join()
    queue_thread.join()