import httpx
from config import settings

async def take_movie_rating(title: str):
    if not settings.OMDB_API_KEY:
        return None
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://www.omdbapi.com/", params={'t': title, 'apikey': settings.OMDB_API_KEY})
            data = response.json()
            if data.get("Response") != "True":
                return None
            rating = data.get("imdbRating")
            if rating and rating != "N/A":
                return float(rating)
            return None
    except Exception:
        return None