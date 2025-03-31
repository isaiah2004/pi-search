from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from src.search_service import process_search_request
from src.index_to_cipher import index_to_cipher
from src.decipher import decipher,validate_input_string
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class SearchRequest(BaseModel):
    input_string: str

class DecipherRequest(BaseModel):
    input_string: str


class SearchResponse(BaseModel):
    encrypted_string: str
    # indexes: list  # Changed from list to dict
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

        # Validate input string

        logger.info(re.fullmatch(r"[a-zA-Z !?.,;\\-]+", request.input_string))
        if not re.fullmatch(r"[a-zA-Z !?.,;\\-]+", request.input_string):
            logger.info(f"Unsupported input: {request.input_string}")
            raise HTTPException(
            status_code=400,
            detail="Functionality not supported for input containing non-alphabetic characters other than spaces.",
            )

        logger.info(f"Processing search request for: {request.input_string}")

        result = process_search_request(request.input_string)
        encrypted_string = index_to_cipher(result)
        # No need to extract indexes from the dictionary anymore
        # logger.info(f"Search completed. Found at indexes: {result}")
        # return SearchResponse( encrypted_string=encrypted_string, indexes=result, message="Search completed successfully.")
        return SearchResponse(
            encrypted_string=encrypted_string, message="Search completed successfully."
        )
    except Exception as e:
        logger.error(f"Error processing search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/decipher")
async def decipher_string(request: DecipherRequest):
    try:
        if not validate_input_string(request.input_string):
            raise HTTPException(
                status_code=400,
                detail="Invalid input string. Please provide a valid string.",
            )
        deciphered_string = decipher(request.input_string)
        return {"deciphered_string": deciphered_string}
    except Exception as e:
        logger.error(f"Error deciphering string: {str(e)}")
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
