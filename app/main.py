# app/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.api.v1.task import router as task_router

app = FastAPI(title="Task API", version="1.0.0", description="CRUD API")


# Handle all ValidationError (typically raised by pydantic validation)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


# Handle all custom HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# Handle fallback for ANY other Exception
@app.exception_handler(Exception)
async def fallback_exception_handler(request: Request, exc: Exception):
    # Here you might want to log the error somewhere
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )


# 註冊 router
app.include_router(task_router, prefix="/api/v1/tasks")

# 啟動後可以透過:
# http://localhost:8000/docs 觀看 swagger UI
# http://localhost:8000/redoc 觀看 ReDoc
