from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongo_url: str
    mongo_db_name: str
    openai_api_key: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"  
    jwt_access_token_exp_minutes: int = 30  
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
