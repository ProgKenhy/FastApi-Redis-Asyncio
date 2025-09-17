from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from config.auth import get_password_hash, verify_password, create_access_token
from tasks.router import task_router
from fastapi.security import OAuth2PasswordRequestForm

api_router = APIRouter()

api_router.include_router(task_router)

users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash("admin123"),
    }
}


@api_router.post("/auth/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    return {"access_token": token, "token_type": "bearer"}


@api_router.get("/health/")
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "task_service"}
    )