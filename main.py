from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import requests
import os
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Segment (CDP) Demo API",
    description="Server-side API for real-time event tracking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SEGMENT_WRITE_KEY = os.getenv("SEGMENT_WRITE_KEY", "")
API_KEYS = os.getenv("API_KEYS", "").split(",")
BASE_DOMAIN = os.getenv("BASE_DOMAIN", "")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def validate_api_key(api_key: str = Depends(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key missing"
        )
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return api_key

from routers.keycard import keycard as keycard_routes
from routers.registration import registration as registration_routes

app.include_router(keycard_routes)
app.include_router(registration_routes)
