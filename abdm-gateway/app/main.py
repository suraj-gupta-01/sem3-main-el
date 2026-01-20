from fastapi import FastAPI 
from loguru import logger 
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.api.routes import api_router

settings = get_settings()
configure_logging(settings.log_level)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    logger.info(f"Starting ADBM Gateway on {settings.app_host}:{settings.app_port}")
    logger.info(f"Environment: {settings.app_env}")

    yield  # App runs here

    # --- Shutdown ---
    logger.info("Shutting down ABDM Gateway")


app = FastAPI(
    title="ABDM Gateway",
    description="API Gateway for ABDM services",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "abdm-gateway"}

@app.get("/hello")
async def hello():
    return {"message": "Hello, ABDM Gateway!"}
