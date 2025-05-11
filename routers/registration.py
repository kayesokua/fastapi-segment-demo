from fastapi import APIRouter, Depends, Request
from models.registration import UserIdentifyModel, NewMemberContractEvent, UserSampleModel
from main import validate_api_key
from main import SEGMENT_WRITE_KEY, BASE_DOMAIN
import requests
import logging
from datetime import date, datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

registration = APIRouter()

@registration.post("/user/register/new-member", tags=["member-registration"])
async def new_member_registration(
    event_model: UserIdentifyModel,
    request: Request, 
    api_key: str = Depends(validate_api_key)):
    try:

        identify_response = requests.post(
            "https://api.segment.io/v1/identify",
            json={
                "userId": str(event_model.userId),
                "traits": {
                    "id": str(event_model.traits["id"]),
                    "firstName": str(event_model.traits["firstName"]),
                    "lastName": str(event_model.traits["lastName"]),
                    "email": str(event_model.traits["email"]),
                    "birthday": event_model.traits["birthday"].date(),
                    "gender": str(event_model.traits["gender"]),
                    "age": str(event_model.traits["age"]),
                    "address": {
                        "zipCode": str(event_model.traits["address"].get("zipCode")),
                        "state": str(event_model.traits["address"].get("state")), 
                        "country_alpha2": str(event_model.traits["address"].get("country_alpha2")), 
                    },
                    "phone": str(event_model.traits["phone"]), 
                    "createdAt": date.today().isoformat(), 
                },
                "timestamp": datetime.now()
            },
            auth=(SEGMENT_WRITE_KEY, "")
        )
        print(identify_response.raise_for_status())

    except requests.RequestException as e:
        logger.error(f"Segment error: {e}")
        return {
            "status": "error",
            "message": str(e),
            "docs": f"{BASE_DOMAIN}/docs"
        }

    return {
        "status": "success",
        "message": "Event processed successfully",
        "docs": f"{BASE_DOMAIN}/docs"
    }

@registration.post("/user/register/new-contract", tags=["member-registration"])
async def new_member_registration_contract(
    event_model: NewMemberContractEvent,
    request: Request, 
    api_key: str = Depends(validate_api_key)):
    try:
        user_agent = request.headers.get("user-agent", "")
        device_info = {
            "user_agent": user_agent,
            "ip_address": request.client.host if request.client else None,
            **event_model.context.device 
        }

        contract_event_response = requests.post(
            "https://api.segment.io/v1/track",
            json={
                "userId": str(event_model.userId),
                "event": "signup_contract_created",
                "properties": {
                    "tarifName": event_model.properties.tarifName,
                    "tarifFee": event_model.properties.tarifFee,
                    "currency": event_model.currency,
                    "startDate": event_model.properties.startDate.isoformat(),
                },
                "context": {
                    "device": device_info,
                    "ip": request.client.host if request.client else None,
                    "userAgent": user_agent
                }
            },
            auth=(SEGMENT_WRITE_KEY, "")
        )
        contract_event_response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Segment error: {e}")
        return {
            "status": "error",
            "message": str(e),
            "docs": f"{BASE_DOMAIN}/docs"
        }

    return {
        "status": "success",
        "message": "Event processed successfully",
        "docs": f"{BASE_DOMAIN}/docs"
    }


@registration.post("/user/register/sample", tags=["member-registration"])
async def sample_indetify_event(
    event_model: UserSampleModel,
    request: Request, 
    api_key: str = Depends(validate_api_key)):
    try:
    
        segment_identify = requests.post(
            "https://api.segment.io/v1/identify",
            json={
                    "userId": "019mr8mf4r",
                    "traits": {
                        "email": "pgibbons@example.com",
                        "name": "Peter Gibbons",
                        "industry": "Technology"
                    },
                    "context": {
                        "ip": "24.5.68.47"
                    },
                    "timestamp": "2012-12-02T00:30:08.276Z",
                    "integrations": {
                        "All": False,
                        "Mixpanel": True,
                        "Kissmetrics": True,
                        "Google Analytics": False
                    }
            },
            auth=(SEGMENT_WRITE_KEY, "")
        )
        segment_identify.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Segment error: {e}")
        return {
            "status": "error",
            "message": str(e),
            "docs": f"{BASE_DOMAIN}/docs"
        }

    return {
        "status": "success",
        "message": "Event processed successfully",
        "docs": f"{BASE_DOMAIN}/docs"
    }