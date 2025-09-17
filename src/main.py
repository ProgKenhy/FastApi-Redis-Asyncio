import sys
from pathlib import Path
from logging import getLogger
from logging_setup import setup_logging

setup_logging()
logger = getLogger(__name__)

sys.path.append(str(Path(__file__).resolve().parent))

import uvicorn
from fastapi import FastAPI
from config.router import api_router

app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
