from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, Literal, Dict, Any

class AddressModel(BaseModel):
    zipCode: str = Field(..., example="10315")
    state: str = Field(..., example="Berlin")
    country_alpha2: str = Field(..., min_length=2, max_length=2, example="DE")

class UserTraitsModel(BaseModel):
    id: str = Field(..., example="B0027-14602")
    firstName: str = Field(..., example="Kaye")
    lastName: str = Field(..., example="So Kua")
    email: EmailStr = Field(..., example="learnwithkaye@gmail.com")
    birthday: date = Field(..., example="2000-12-25")
    gender: str = Field(..., example="F", min_length=1, max_length=1)
    address: AddressModel
    phone: str = Field(..., example="+4901234567")
    createdAt: datetime = Field(default_factory=datetime.now)
    
    age: Optional[int] = Field(None, example=23)
    
    @field_validator('age', mode='before')
    def calculate_age(cls, v, values):
        if v is not None:
            return v
            
        if 'birthday' not in values:
            raise ValueError("birthday is required for age calculation")
            
        today = date.today()
        birthday = values['birthday']
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        return age

class UserIdentifyModel(BaseModel):
    type: str = Field(default="identify", example="identify")
    userId: str = Field(..., example="B0027-14602")
    traits: UserTraitsModel

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }
        json_schema_extra = {
            "example": {
                "type": "identify",
                "userId": "B0027-14602",
                "traits": {
                    "id": "B0027-14602",
                    "firstName": "Kaye",
                    "lastName": "Kua",
                    "email": "example@gmail.com",
                    "birthday": "2000-12-25",
                    "gender": "F",
                    "address": {
                        "zipCode": "10117",
                        "state": "Berlin",
                        "country_alpha2": "DE",
                    },
                    "phone": "+4901234567",
                    "createdAt": datetime.now().isoformat(),
                }
            }
        }

class EventContext(BaseModel):
    device: Dict[str, Any] = Field(
        default_factory=dict,
        example={
            "brand": "Apple",
            "model": "iPhone 13",
            "type": "mobile",
            "os": "iOS 15"
        },
        description="Device information dictionary that can contain any key-value pairs"
    )

class NewContractProperties(BaseModel):
    tarifName: str = Field(..., example="FLEX SPECIAL INKL. PILATES")
    tarifFee: float = Field(..., example=10.00)
    startDate: date = Field(default_factory=date.today)

class NewMemberContractEvent(BaseModel):
    type: Literal["track"] = Field(default="track", example="track")
    userId: str = Field(..., example="B0027-14602")
    event: str = Field(default="signup_contract_created", example="signup_contract_created")
    currency: str = Field(default="EUR", example="EUR", min_length=3, max_length=3)
    properties: NewContractProperties
    context: EventContext = Field(default_factory=EventContext)

    class Config:
        json_schema_extra = {
            "example": {
                "type": "track",
                "userId": "B0027-14602",
                "event": "signup_contract_created",
                "currency": "EUR",
                "properties": {
                    "tarifName": "FLEX SPECIAL INKL. PILATES",
                    "tarifFee": 10.00,
                    "startDate": date.today().isoformat()
                }
            }
        }