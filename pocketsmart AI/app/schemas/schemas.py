from typing import Optional, List

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
)


class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=120,
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=128,
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0
    )

    style: str = "Modern"

    rooms: List[str] = []

    items: List[str] = []

    city: str = "Chennai"


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0
    )

    guests: int = Field(
        gt=0,
        le=10000,
    )

    event_type: str = "Birthday"

    venue: str = "Home"

    city: str = "Chennai"


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0
    )

    occasion: str = "Wedding"

    style: str = "Elegant"

    outfit_color: Optional[str] = None

    outfit_description: Optional[str] = None


class RecommendationItem(BaseModel):

    category: str

    name: str

    description: str

    price: float

    platform: str

    url: str


class RecommendationResponse(BaseModel):

    planner: str

    budget: float

    allocated_total: float

    summary: str

    tips: List[str]

    recommendations: List[RecommendationItem]

    source: str