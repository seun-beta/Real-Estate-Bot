from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vertexai.language_models import TextGenerationModel
import sqlite3
from typing import Dict

app = FastAPI()

# Initialize the text generation model
generation_model = TextGenerationModel.from_pretrained("text-bison@001")


# Pydantic model for user input
class PropertyInquiry(BaseModel):
    description: str


# Function to query the database
def query_properties(entities: Dict[str, str]):
    conn = sqlite3.connect("properties.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM properties WHERE rooms=? AND location LIKE ? AND rent<=?",
        (int(entities["rooms"]), f"%{entities['location']}%", int(entities["rent"])),
    )
    properties = cursor.fetchall()
    conn.close()
    return properties


# Zero-shot prompting
def extract_entities_zero_shot(description: str) -> Dict[str, str]:
    prompt = f"""Description: "{description}"
    As a real estate agent, please extract the following entities from the property description provided: 'rooms', 'location', and 'rent'. Identify the number of rooms, the property's location within Nigeria, and the annual rent expressed in Naira."""
    response = generation_model.predict(prompt)
    entities = eval(response.text.strip().split('Entities: ')[1])
    print(entities)
    return entities


@app.post("/search_properties/zero_shot/")
async def search_properties_zero_shot(inquiry: PropertyInquiry):
    entities = extract_entities_zero_shot(inquiry.description)
    results = query_properties(entities)
    return {"results": results}


# Single-shot prompting
def extract_entities_single_shot(description: str) -> Dict[str, str]:
    prompt = f"""As a real estate agent, you are tasked with extracting essential information from property descriptions. Your job is to identify and list entities related to the number of rooms, location within Nigeria, and the annual rent in Naira. Here is how you should format your response based on the description provided:

    Example: 
    Description: "I need a 3-bedroom house in Lagos for N2,000,000 per year."
    Entities: {{"rooms": "3", "location": "Lagos", "rent": "2000000"}}

    Now, analyze the following description and extract the relevant entities:
    Description: "{description}"
    Extract the entities by pinpointing the number of rooms, the location in Nigeria, and the specified annual rent in Naira."""

    response = generation_model.predict(prompt)
    entities = eval(response.text.strip().split('Entities: ')[1])
    return entities


@app.post("/search_properties/single_shot/")
async def search_properties_single_shot(inquiry: PropertyInquiry):
    entities = extract_entities_single_shot(inquiry.description)
    results = query_properties(entities)
    return {"results": results}


# Few-shot prompting
def extract_entities_few_shot(description: str) -> Dict[str, str]:
    prompt = f"""As a real estate agent specializing in properties across Nigeria, your task is to extract key information from property descriptions. Focus on identifying the number of rooms, location, and annual rent (in Naira). Here are examples of how to extract these entities from descriptions:

    Example 1: 
    Description: "Looking for a 2-bedroom flat in Abuja for N1,500,000 yearly."
    Entities: {{"rooms": "2", "location": "Abuja", "rent": "1500000"}}

    Example 2:
    Description: "I want a 4-bedroom bungalow in Port Harcourt for N3,000,000 annually."
    Entities: {{"rooms": "4", "location": "Port Harcourt", "rent": "3000000"}}

    Your task:
    Description: "{description}"
    Extract the entities by identifying the number of rooms, the specific location in Nigeria, and the annual rent expressed in Naira."""
    response = generation_model.predict(prompt)
    entities = eval(response.text.strip().split('Entities: ')[1])
    return entities


@app.post("/search_properties/few_shot/")
async def search_properties_few_shot(inquiry: PropertyInquiry):
    entities = extract_entities_few_shot(inquiry.description)
    results = query_properties(entities)
    return {"results": results}


# Run the server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
