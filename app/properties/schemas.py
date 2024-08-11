from typing import List

from pydantic import BaseModel


class PropertyInquiry(BaseModel):
    description: str


class PropertySchema(BaseModel):
    rooms: int
    location: str
    rent: int


class PropertyListResponse(BaseModel):
    results: List[PropertySchema]
