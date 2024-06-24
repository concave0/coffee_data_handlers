from fastapi import FastAPI 
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from routes import router , auth_token
import uvicorn
import os 
import os
from threading import Thread 
from prometheus_fastapi_instrumentator import Instrumentator
from give_token import TokenInTransit
from dotenv import load_dotenv
from trigger_data_collection import TriggerDataCollection
from triggering_condition import Constient_Condition_Trigger
from recieve_token import CONSTAINT_WEBSITE_TOKEN

# Server Config
app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(router=router)

limiter = Limiter(key_func=get_remote_address, default_limits=["80/seconds"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Prometheus metrics middleware config 
instrumentator = Instrumentator().instrument(app).expose(app , include_in_schema=False)
instrumentator.should_group_status_codes = True 
instrumentator.should_exclude_streaming_duration = True
instrumentator.should_instrument_requests_inprogress = True 


def run_send_token():
    print("Starting sending token")
    env = load_dotenv()
    development_url_need_to_be_changed = os.environ['development_url_need_to_be_changed_api_key'] # temp replit endpoint  
    in_transit  = TokenInTransit()
    in_transit.give(token=auth_token.token, endpoint=development_url_need_to_be_changed)

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8080)

def run_trigger_condition(): 
    import time 
    time.sleep(10)
 
    if Constient_Condition_Trigger.trigger_or_not_to == False: 
        development_url_need_to_be_changed = os.environ['development_url_need_to_be_changed_data_collection'] # temp replit endpoint  
        print(f"target endpiont url {development_url_need_to_be_changed}")
        trigger_datacollection = TriggerDataCollection()
        token = CONSTAINT_WEBSITE_TOKEN.curr_token
        results = trigger_datacollection.triggering(token=token , endpoint=development_url_need_to_be_changed) #  triger data collection 
        print(f"Sent this token and the response was {results.status_code}")

if __name__ =="__main__": 
    server_thread = Thread(target=run_server) 
    token_thread = Thread(target=run_send_token)
    thread_run_trigger_condition = Thread(target=run_trigger_condition)

    server_thread.start()
    token_thread.start()
    thread_run_trigger_condition.start()

    server_thread.join()
    token_thread.join()
    thread_run_trigger_condition.start()


