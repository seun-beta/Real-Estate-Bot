# House Rental Search API

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

This project is designed to provide an API for a house rental service that enables users to find properties based on descriptions. It utilizes a state-of-the-art language model from Vertex AI to extract key information such as the number of rooms, location, and rent from natural language descriptions. The API then queries a pre-populated SQLite database to find matching properties based on the extracted data.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- FastAPI
- Uvicorn, an ASGI server for running FastAPI
- SQLite3 for the database
- vertexai for integrating with Google Vertex AI

You can install the necessary libraries with pip:

```bash
pip install fastapi uvicorn sqlite3 vertexai
```

Additionally, you will need to obtain a `credentials.json` file for accessing Google Cloud services:
- Download the `credentials.json` from your Google Cloud Platform console.
- Place the `credentials.json` in your project directory, or a secure location of your choice.
- [Download credentials.json here](https://drive.google.com/file/d/1fFKOEwhG6ockH_aGBatH_zpEFgP38piH/view?usp=sharing)  
### Installing

Follow these steps to get your development environment running:

1. Clone the repository to your local machine:

```bash
git clone https://yourrepository.com/yourproject.git
cd yourproject
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Set up the environment variable for Google Cloud credentials:

```bash
export GOOGLE_APPLICATION_CREDENTIALS='path/to/your/credentials.json'
```

4. Initialize the database with the seed data:

```bash
python seed.py
```

5. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

This will start the server on `http://127.0.0.1:8000`. You can interact with the API using this base URL.

## Usage <a name = "usage"></a>

To use the API, send HTTP requests to the appropriate endpoints:

- **Zero-Shot Prompting Endpoint:**
  - `POST /search_properties/zero_shot/`
  - Description: Pass a property description and receive property matches without prior examples.

- **Single-Shot Prompting Endpoint:**
  - `POST /search_properties/single_shot/`
  - Description: Pass a property description with a single example to guide the model.

- **Few-Shot Prompting Endpoint:**
  - `POST /search_properties/few_shot/`
  - Description: Pass a property description along with multiple examples to help the model understand the context better.

For example, to query the few-shot endpoint, you might use a tool like `curl`:

```bash
curl -X 'POST' \
  'http://localhost:8000/search_properties/few_shot/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "Searching for a 3-bedroom house in Lagos with a budget of N3,500,000."
}'
```

This sends a description to the API and retrieves matching properties based on the specified criteria.


