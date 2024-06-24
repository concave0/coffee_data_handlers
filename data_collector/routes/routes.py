from fastapi import APIRouter , Request , Response
from fastapi.responses import FileResponse 
from prometheus_client.exposition import choose_encoder , REGISTRY

# Router 
router = APIRouter()

# Checking if its up in general endpoint
@router.get("/")
async def is_up(): 
    return {"i am" : "running"}

# Serve raw data to other appilcations via 
@router.get("/get_data_wiki")
async def get_wiki_data(request: Request): 
    data = "raw_data/raw_data.json"
    return FileResponse(data, media_type="application/octet-stream", filename=data)

# Metrics endpoint for Prometheus
@router.get("/metrics")
async def metrics(request: Request):
    encoder, content_type = choose_encoder(request.headers.get("Accept"))
    output = encoder(REGISTRY)
    return Response(content=output, media_type=content_type)







