import asyncio
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from src import logger
from src import settings
from src import Base
from src.task.models import TaskStatus
from src.task.router import router as task_router

app = FastAPI(
    debug=True,
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # Allows all origins
allow_credentials=True,
allow_methods=["*"], # Allows all methods
allow_headers=["*"], # Allows all headers
)

app.include_router(task_router)

async def catch_exceptions_middleware(request: Request, call_next):
    """Обработчик внезапных исключений."""
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error(f"Unexpected error on {request.url}: {exc}", exc_info=exc)
        return JSONResponse(
            DefaultResponse(error=True, message=str(exc)).dict(), status_code=200
        )
