import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.api.v1.TaskRouter import task_router
from app.utils.logger import error_logger, access_logger

app = FastAPI(title="Task API", version="1.0.0", description="CRUD API")


# Middleware 記錄每支 API call
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    log_msg = (
        f"{request.method} {request.url.path} - status_code: {response.status_code} - duration: {process_time:.2f}ms"
    )
    access_logger.info(log_msg)
    return response


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    error_logger.warning(f"Validation error: {exc.errors()} - path: {request.url.path}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_logger.error(f"HTTP exception: {exc.detail} - status_code: {exc.status_code} - path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def fallback_exception_handler(request: Request, exc: Exception):
    error_logger.error(f"Unhandled error: {str(exc)} - path: {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )


app.include_router(task_router, prefix="/api/v1/tasks")
