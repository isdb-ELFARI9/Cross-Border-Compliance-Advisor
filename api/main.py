"""
Main entry point for running the API.
"""

import uvicorn
from api.core.config import API_HOST, API_PORT, DEBUG

if __name__ == "__main__":
    uvicorn.run("api.core.app:app", host=API_HOST, port=API_PORT, reload=DEBUG)
