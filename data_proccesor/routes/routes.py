from fastapi import APIRouter , Request , Response 
import json
from prometheus_client.exposition import choose_encoder , REGISTRY

# IDs 
router = APIRouter()

# Sending metrics IDs (is called by the Ngork endpoint)
@router.get("/give_ids")
def sending_ids(request: Request): 
    path = "routes/ids_data/ids.json"
    with open(path, "r") as file: 
        ids = json.loads(json.dumps(json.load(file),indent=4))
    file.close()
    return ids 

# Metrics endpoint that feeds data to prometheus
@router.get("/metrics")
async def metrics(request: Request): 
    encoder, content_type = choose_encoder(request.headers.get("Accept"))
    output = encoder(REGISTRY)
    return Response(content=output, media_type=content_type)





