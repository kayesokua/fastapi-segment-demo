import random
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Literal, Optional

class EventProperties(BaseModel):
    cardId: str
    reason: Literal["active_member","insufficient_membership_tier","expired_membership","idle_membership"]
    direction: Literal["inbound", "outbound"]

class EventContext(BaseModel):
    device: Dict[str,str]

class GymEntryGrantedEvent(BaseModel):
    userId: str = Field(..., min_length=5)
    type: Literal["track"]
    event: Literal["gym_entry_granted"]
    properties: EventProperties
    context: EventContext
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "userId": "B0027-14602",
                "type": "track",
                "event": "gym_entry_granted",
                "properties": {
                    "cardId": "HID-987654321",
                    "reason": "active_member",
                    "direction": random.choice(["inbound","outbound"]),
                },
                "context": {
                    "device": {
                        "cardReaderId": "TDR-B0027-01",
                        "branchId": "B0027",
                        "branchName": "John Reed Berlin-Friedrichain"
                    }
                },
                "timestamp": datetime.now(),
            }
        }

class GymEntryDeniedEvent(BaseModel):
    userId: str = Field(..., min_length=5)
    type: Literal["track"]
    event: Literal["gym_entry_denied"]
    properties: EventProperties
    context: EventContext
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "userId": "B0027-14602",
                "type": "track",
                "event": "gym_entry_denied",
                "properties": {
                    "cardId": "HID-987654321",
                    "reason": random.choice(["insufficient_membership_tier","expired_membership","idle_membership"]),
                    "direction": random.choice(["inbound","outbound"]),
                },
                "context": {
                    "device": {
                        "cardReaderId": "TDR-B0027-01",
                        "branchId": "B0027",
                        "branchName": "John Reed Berlin-Friedrichain"
                    }
                },
                "timestamp": datetime.now(),
            }
        }