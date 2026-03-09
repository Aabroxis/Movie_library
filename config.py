from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "" 
    DB_NAME: str = "movie_library"
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_TIME_LIMIT_MINUTES: int = 30
    OMDB_API_KEY: str = ""
    ADMIN_SECRET: str = ""
    
    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()