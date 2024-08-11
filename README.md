
<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>



---

<p align="center">This project is an AI-powered real estate property search platform built with FastAPI and MongoDB. It leverages OpenAI's GPT model to provide personalized property recommendations based on natural language descriptions and user preferences.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [File Structure](#file_structure)
- [Contributing](#contributing)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

The Real Estate Property Search platform allows users to search for properties using natural language descriptions. The platform utilizes OpenAI's GPT model to extract key information such as the number of rooms, location, and rent from user descriptions. These details are then used to query a MongoDB database to find matching properties. The system also incorporates user preferences to enhance search results, providing personalized recommendations tailored to each user's needs.

## 🏁 Getting Started <a name = "getting_started"></a>

Follow these instructions to set up the project locally for development and testing purposes.

### Prerequisites

Ensure you have the following software installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- An OpenAI API Key (Sign up at [OpenAI](https://beta.openai.com/signup/))

### Installing

1. **Clone the repository:**

   ```bash
   git clone https://github.com/seun-beta/real-estate-ai.git
   cd real-estate-ai
   ```

2. **Create a `.env` file in the root directory:**

   ```env
   MONGO_URL=mongodb://localhost:27017
   MONGO_DB_NAME=real_estate_db
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   JWT_SECRET=supersecretkey
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXP_MINUTES=30
   ```

3. **Build and start the Docker containers:**

   ```bash
   docker-compose up --build
   ```

4. **Access the application:**

   The application will be running at `http://localhost:8000`.

## 🎈 Usage <a name="usage"></a>

Once the application is running, you can:

- **Register/Login**: Use the `/users/register` and `/users/login` endpoints to create an account and authenticate.
- **Set Preferences**: Set your property search preferences using the `/users/preferences/` endpoint.
- **Search Properties**: Use the `/properties/search_properties/` endpoints to search for properties based on natural language descriptions. The platform supports zero-shot, single-shot, and few-shot learning techniques for entity extraction.

### API Endpoints

#### **User Endpoints:**

- **POST** `/users/register`: Register a new user.
- **POST** `/users/login`: Login and receive a JWT token.
- **POST** `/users/preferences/`: Set user preferences for property search.
- **GET** `/users/preferences/`: Get the current user’s property search preferences.

#### **Property Search Endpoints:**

- **POST** `/properties/search_properties/zero_shot/`: Search properties using zero-shot learning.
- **POST** `/properties/search_properties/single_shot/`: Search properties using single-shot learning.
- **POST** `/properties/search_properties/few_shot/`: Search properties using few-shot learning.

## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.python.org/) - Programming Language
- [FastAPI](https://fastapi.tiangolo.com/) - Web Framework
- [MongoDB](https://www.mongodb.com/) - Database
- [Docker](https://www.docker.com/) - Containerization
- [OpenAI GPT](https://openai.com/) - AI Model

## 🗂️ File Structure <a name = "file_structure"></a>

```
.
├── app
│   ├── config.py             # Configuration settings
│   ├── users
│   │   ├── models.py         # User and UserPreference models
│   │   ├── schemas.py        # User and UserPreference schemas
│   │   ├── routers.py        # User routes including registration, login, and preferences
│   │   ├── auth.py           # User authentication utilities
│   ├── properties
│   │   ├── models.py         # Property model
│   │   ├── schemas.py        # PropertyInquiry and PropertyListResponse schemas
│   │   ├── routers.py        # Property search routes
├── main.py                   # FastAPI application initialization
├── requirements.txt          # Python dependencies
├── Dockerfile                # Dockerfile for FastAPI app
├── docker-compose.yml        # Docker Compose file
├── .env                      # Environment variables
└── README.md                 # Project documentation
```

## 🤝 Contributing <a name = "contributing"></a>

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/seun-beta/real-estate-ai/issues).

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a pull request

## ✍️ Authors <a name = "authors"></a>

- [@seun-beta](https://github.com/seun-beta) - Idea & Initial work

See also the list of [contributors](https://github.com/seun-beta/real-estate-ai/contributors) who participated in this project.

## 🎉 Acknowledgments <a name = "acknowledgement"></a>

- Thanks to the FastAPI community for their invaluable documentation.
- Special thanks to OpenAI for providing the GPT model.
- Inspiration from modern real estate platforms and AI-driven applications.
