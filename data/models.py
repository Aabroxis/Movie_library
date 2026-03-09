from pydantic import Field, BaseModel, field_validator
from typing import Optional

class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    director: Optional[str] = None
    release_year: Optional[int] = None
    
    @field_validator("release_year")
    @classmethod
    def valid_year(cls, year):
        if year is not None and not (1888 <= year <= 2030):
            raise ValueError("Release year must be between 1888 and 2030")
        return year
    
class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length= 255)
    director: Optional[str] = None
    release_year: Optional[int] = None
    
    @field_validator("release_year")
    @classmethod
    def valid_year(cls, year):
        if year is not None and not (1888 <= year <= 2030):
            raise ValueError("Release year must be between 1888 and 2030")
        return year
    
class MovieResponse(BaseModel):
    id: int
    title: str
    director: Optional[str]
    release_year: Optional[int]
    rating: Optional[float]
    
class CreateUser(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6)
    role: str = Field(default="USER", pattern="^(ADMIN|USER)$")
    admin_secret: Optional[str] = None

class Token(BaseModel):
    access_token: str 
    token_type: str = "baerer"
    
class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
    
