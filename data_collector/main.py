from threading import Thread 

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_client import make_asgi_app , CollectorRegistry 
from prometheus_fastapi_instrumentator import Instrumentator

from routes.routes import router  
from workers.worker import Worker 

# Config for server
app =  FastAPI()
app.include_router(router)

# Prometheus metrics middleware config 
instrumentator = Instrumentator().instrument(app).expose(app , include_in_schema=False)
instrumentator.should_group_status_codes = True 
instrumentator.should_exclude_streaming_duration = True
instrumentator.should_instrument_requests_inprogress = True 

# Create a new registry for each process
def make_metrics_app():
    registry = CollectorRegistry()
    return make_asgi_app(registry=registry)

# Add GZip middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Thread Functions
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8001)

def run_workers(): 
    worker  = Worker()
    worker.set_jobs()
    worker.scheduler.start()


if __name__ == "__main__": 
    server_thread = Thread(target=run_server)
    # scheduler_thread = Thread(target=run_workers)

    server_thread.start()
    # scheduler_thread.start()

    server_thread.join()
    # scheduler_thread.join()
