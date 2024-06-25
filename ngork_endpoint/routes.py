from fastapi import  APIRouter, Response , Request , Depends
from recieve_token import CONSTAINT_WEBSITE_TOKEN
import requests 
from prometheus_client.exposition import choose_encoder , REGISTRY
from fastapi.security import OAuth2PasswordBearer
import secrets
import string
import os
import datetime
from triggering_condition import Constient_Condition_Trigger


router = APIRouter()

# Diagnostic endpoint to see if the server is up 
@router.get("/")
def redirected_service(request: Request): 
    return {"iam":"up"} 

# Generate JWT Token for Authentication
class GenerateAuthToken:
    def __init__(self) -> None:
        self.token = self.generate_token(32) # meant to be shared with unit tests
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=self.token)
        self.enivorment = self.set_enivorment_variable()
        self.SECRET_KEY = self.token 
        self.ALGORITHM = "HS256"  

    def generate_token(self, length:int):
        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for _ in range(length))
        return token

    def set_enivorment_variable(self): 
        os.environ["API_KEY"] = self.token
        print(f"set enivormental variable {self.token}")

# Handling Authentication 
auth_token = GenerateAuthToken()

# Auth Endpoint
async def get_app(token: str = Depends(auth_token.oauth2_scheme)):
    pass 
  

# Router endpoint to ether database or data proccessor for data collection or id collection
@router.get("/ngork_endpoint/{wanted_directed_service}")
async def redirected_service(request: Request, wanted_directed_service:str , app_auth: str = Depends(get_app)): 
    if wanted_directed_service=="id": 
        url = "http://0.0.0.0:8006/give_ids"
        response = requests.get(url)
        data = response.json()  
        return data

    elif wanted_directed_service=="data": 
        try: 
            specfic_coffee_id = int(request.headers.get("X-Request-ID"))  # checking headers for specfic_coffee_id
            print(specfic_coffee_id)
            url= f"http://0.0.0.0:8003/request_data/{specfic_coffee_id}"
            response = requests.get(url)
            data = response.json()
            return data 
        except Exception as e: 
            now = datetime.datetime.now()
            print(f"{e} happened at {now}")

# Accepting tokens from the coffee website 
@router.post("/updating_api_key")
async def recieve_api_key(request: Request):
    new_token = str(request.headers.get("Authorization")).split(" ") # Recieve websites token and then stores 
    CONSTAINT_WEBSITE_TOKEN.curr_token = new_token 
    print(f"websites token {CONSTAINT_WEBSITE_TOKEN.curr_token[1]} and the ngrok token is {auth_token.token}")
    Constient_Condition_Trigger.trigger_or_not_to = False 
    response_confirm  = Response(content="Got the token", status_code=200)
    return response_confirm


# Give meterics to Prometheus
@router.get("/metrics")
async def metrics(request: Request): 
    encoder, content_type = choose_encoder(request.headers.get("Accept"))
    output = encoder(REGISTRY)
    return Response(content=output, media_type=content_type)
