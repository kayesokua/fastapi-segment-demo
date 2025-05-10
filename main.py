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
    title="Segment CDP Demo API",
    description="API for Segment CDP integration with Cloud Function processing",
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

class TrackEvent(BaseModel):
    user_id: str
    event: str
    properties: dict = {}
    context: Optional[dict] = None
    anonymous_id: Optional[str] = None

class IdentifyEvent(BaseModel):
    user_id: str
    traits: dict = {}
    context: Optional[dict] = None
    anonymous_id: Optional[str] = None

# Endpoints
@app.post("/track", summary="Track a Segment event")
async def track_event(
    event: TrackEvent,
    request: Request,
    api_key: str = Depends(validate_api_key)
):
    """
    Track an event to Segment with optional Function processing
    """
    try:
        segment_event = {
            "userId": event.user_id,
            "anonymousId": event.anonymous_id,
            "event": event.event,
            "properties": event.properties,
            "context": {
                "ip": request.client.host,
                "userAgent": request.headers.get("user-agent"),
                "library": {
                    "name": "segment-fastapi-demo",
                    "version": "1.0.0"
                },
                **(event.context or {})
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        # Send to Segment
        response = requests.post(
            "https://api.segment.io/v1/track",
            json=segment_event,
            auth=(SEGMENT_WRITE_KEY, "")
        )

        if response.status_code != 200:
            logger.error(f"Segment API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=502,
                detail="Segment API request failed"
            )

        return {
            "status": "success",
            "message": "Event processed",
            "event_id": response.json().get("messageId"),
            "docs": f"{BASE_DOMAIN}/docs"
        }

    except Exception as e:
        logger.exception("Error processing track event")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/identify", summary="Identify a user in Segment")
async def identify_user(
    event: IdentifyEvent,
    request: Request,
    api_key: str = Depends(validate_api_key)
):
    """
    Identify a user to Segment with optional Function processing
    """
    try:
        segment_event = {
            "userId": event.user_id,
            "anonymousId": event.anonymous_id,
            "traits": event.traits,
            "context": {
                "ip": request.client.host,
                "userAgent": request.headers.get("user-agent"),
                **(event.context or {})
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        response = requests.post(
            "https://api.segment.io/v1/identify",
            json=segment_event,
            auth=(SEGMENT_WRITE_KEY, "")
        )

        if response.status_code != 200:
            logger.error(f"Segment API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=502,
                detail="Segment API request failed"
            )

        return {
            "status": "success",
            "message": "Identify event processed",
            "event_id": response.json().get("messageId")
        }

    except Exception as e:
        logger.exception("Error processing identify event")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}