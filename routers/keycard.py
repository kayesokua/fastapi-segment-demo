from fastapi import APIRouter, Depends, Request
from models.keycard import GymEntryGrantedEvent, GymEntryDeniedEvent
from main import validate_api_key
from main import SEGMENT_WRITE_KEY, BASE_DOMAIN
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

keycard = APIRouter()

@keycard.post("/user/check-in/granted", tags=["member-entry"])
async def gym_entry_granted(
    event_model: GymEntryGrantedEvent,
    request: Request, 
    api_key: str = Depends(validate_api_key)):
    try:
        requests.post("https://api.segment.io/v1/track",
            json={
                "userId": str(event_model.userId), 
                "event": str(event_model.event),
                "properties": {
                    "cardId": str(event_model.properties.cardId), 
                    "reason": str(event_model.properties.reason),
                    "direction": str(event_model.properties.direction),
                },
                "context": {
                    "device": {
                        "cardReaderId": str(event_model.context.device["cardReaderId"]),
                        "branchId": str(event_model.context.device.get("branchId", "")),
                        "branchName": str(event_model.context.device.get("branchName", "")),
                    }
                },
                "timestamp": event_model.timestamp.isoformat()
            },
            auth=(SEGMENT_WRITE_KEY, "")
        )

    except requests.RequestException as e:
        logger.warning(f"Segment error: {e}")

    return {
        "status": "success",
        "message": "Event processed successfully",
        "docs": f"{BASE_DOMAIN}/docs"
    }

@keycard.post("/user/check-in/denied", tags=["member-entry"])
async def gym_entry_denied(
    event_model: GymEntryDeniedEvent,
    request: Request, 
    api_key: str = Depends(validate_api_key)):
    try:
        requests.post("https://api.segment.io/v1/track",
            json={
                "userId": str(event_model.userId), 
                "event": str(event_model.event),
                "properties": {
                    "cardId": str(event_model.properties.cardId), 
                    "reason": str(event_model.properties.reason),
                    "direction": str(event_model.properties.direction),
                },
                "context": {
                    "device": {
                        "cardReaderId": str(event_model.context.device["cardReaderId"]),
                        "branchId": str(event_model.context.device.get("branchId", "")),
                        "branchName": str(event_model.context.device.get("branchName", "")),
                    }
                },
                "timestamp": event_model.timestamp.isoformat()
            },
            auth=(SEGMENT_WRITE_KEY, "")
        )

    except requests.RequestException as e:
        logger.warning(f"Segment error: {e}")

    return {
        "status": "success",
        "message": "Event processed successfully",
        "docs": f"{BASE_DOMAIN}/docs"
    }