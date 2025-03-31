from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from src.search_service import process_search_request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class SearchRequest(BaseModel):
    input_string: str

class SearchResponse(BaseModel):
    indexes: list
    message: str

@app.get("/")
async def root():
    return {"message": "Pi Search API is running"}

@app.post("/search", response_model=SearchResponse)
async def search_for_string(request: SearchRequest, raw_request: Request):
    try:
        # Log the raw request body for debugging
        body = await raw_request.body()
        logger.info(f"Received request body: {body.decode()}")
        
        logger.info(f"Processing search request for: {request.input_string}")
        indexes = process_search_request(request.input_string)
        return SearchResponse(indexes=indexes, message="Search completed successfully.")
    except Exception as e:
        logger.error(f"Error processing search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request path: {request.url.path}, method: {request.method}")
    try:
        response = await call_next(request)
        logger.info(f"Response status code: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request error: {str(e)}")
        raise