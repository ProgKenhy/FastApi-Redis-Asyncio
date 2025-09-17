import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from fastapi.responses import JSONResponse

import uvicorn
from fastapi import FastAPI
from config.router import api_router

app = FastAPI()


@app.get("/health/")
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "task_service"}
    )


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
