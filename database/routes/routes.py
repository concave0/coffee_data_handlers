from fastapi import APIRouter , Request , Response 
import json
from database.database import  create_new_coffee , get_specfic_coffee_details 
from prometheus_client.exposition import choose_encoder , REGISTRY


# Router 
router = APIRouter()

# Checking if its up in general endpoint
@router.get("/")
def hello_world(): 
    return {"i am" : "running"}

# Getting data 
@router.get("/request_data/{specfic_coffee_id}")
async def request_data(request: Request, specfic_coffee_id: int): 
    coffee= get_specfic_coffee_details(specfic_coffee_id)
    data = { "Id" : f"{coffee.id}",
                "User": f"{coffee.name}",
                "Facts" : f"{coffee.facts}",
                "commit_date" : f"{coffee.commit_date}", 
            }
    return {"Data": data}

# Prometheus Endpoint 
@router.get("/metrics")
async def metrics(request: Request): 
    encoder, content_type = choose_encoder(request.headers.get("Accept"))
    output = encoder(REGISTRY)
    return Response(content=output, media_type=content_type)

