from typing import Dict

from fastapi import APIRouter, Depends
from openai import Completion

from app.config import settings
from app.users.routers import get_current_user
from properties.models import Property
from properties.schemas import PropertyInquiry, PropertyListResponse

router = APIRouter()

generation_model = Completion(api_key=settings.openai_api_key)


def query_properties(entities: Dict[str, str]):
    properties = Property.objects(
        rooms=int(entities["rooms"]),
        location__icontains=entities["location"],
        rent__lte=int(entities["rent"]),
    )
    return properties


def extract_entities(description: str, prompt_template: str) -> Dict[str, str]:
    system_message = "You are a real estate agent in Nigeria. Your task is to extract key details from property descriptions to help match users with available properties."

    prompt = prompt_template.format(description=description)

    response = generation_model.create(
        engine="gpt-4", prompt=prompt, max_tokens=150, temperature=0.7
    )

    entities = eval(response.choices[0].text.strip().split("Entities: ")[1])
    return entities


@router.post("/search_properties/zero_shot/", response_model=PropertyListResponse)
async def search_properties_zero_shot(
    inquiry: PropertyInquiry, current_user=Depends(get_current_user)
):
    prompt_template = """
    Description: "{description}"
    As a real estate agent, please extract the following entities from the property description provided: 'rooms', 'location', and 'rent'. Identify the number of rooms, the property's location within Nigeria, and the annual rent expressed in Naira.
    """
    entities = extract_entities(inquiry.description, prompt_template)
    results = query_properties(entities)
    return {"results": list(results)}


@router.post("/search_properties/single_shot/", response_model=PropertyListResponse)
async def search_properties_single_shot(
    inquiry: PropertyInquiry, current_user=Depends(get_current_user)
):
    prompt_template = """
    As a real estate agent, you are tasked with extracting essential information from property descriptions. Your job is to identify and list entities related to the number of rooms, location within Nigeria, and the annual rent in Naira. Here is how you should format your response based on the description provided:

    Example: 
    Description: "I need a 3-bedroom house in Lagos for N2,000,000 per year."
    Entities: {{"rooms": "3", "location": "Lagos", "rent": "2000000"}}

    Now, analyze the following description and extract the relevant entities:
    Description: "{description}"
    Extract the entities by pinpointing the number of rooms, the location in Nigeria, and the specified annual rent in Naira.
    """
    entities = extract_entities(inquiry.description, prompt_template)
    results = query_properties(entities)
    return {"results": list(results)}


@router.post("/search_properties/few_shot/", response_model=PropertyListResponse)
async def search_properties_few_shot(
    inquiry: PropertyInquiry, current_user=Depends(get_current_user)
):
    prompt_template = """
    As a real estate agent specializing in properties across Nigeria, your task is to extract key information from property descriptions. Focus on identifying the number of rooms, location, and annual rent (in Naira). Here are examples of how to extract these entities from descriptions:

    Example 1: 
    Description: "Looking for a 2-bedroom flat in Abuja for N1,500,000 yearly."
    Entities: {{"rooms": "2", "location": "Abuja", "rent": "1500000"}}

    Example 2:
    Description: "I want a 4-bedroom bungalow in Port Harcourt for N3,000,000 annually."
    Entities: {{"rooms": "4", "location": "Port Harcourt", "rent": "3000000"}}

    Your task:
    Description: "{description}"
    Extract the entities by identifying the number of rooms, the specific location in Nigeria, and the annual rent expressed in Naira.
    """
    entities = extract_entities(inquiry.description, prompt_template)
    results = query_properties(entities)
    return {"results": list(results)}
