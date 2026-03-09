from data.database import insert_query, update_query, read_query
from data.models import MovieUpdate, MovieCreate, MovieResponse
from services.omdb_services import take_movie_rating 

def create_movie(movie_data: MovieCreate):
    movie_id = insert_query("INSERT INTO movies (title, director, release_year) VALUES(?,?,?)",
        (movie_data.title, movie_data.director, movie_data.release_year))
    
    return MovieResponse(
        id = movie_id,
        title = movie_data.title,
        director=movie_data.director,
        release_year=movie_data.release_year,
        rating = None,
    )
    
def get_all_movies(movie_name : str | None = None, sorted_by_rating: bool = False):
    sql = "SELECT id, title, director, release_year, rating FROM movies"
    sql_params = []
    
    if movie_name:
        sql += " WHERE title LIKE ?"
        sql_params.append(f"%{movie_name}%")
    if sorted_by_rating:
        sql += " ORDER BY rating DESC" 
        
    rows = read_query(sql, sql_params)
    movies = []
    
    for row in rows:
        movie = MovieResponse(
            id = row["id"],
            title= row["title"],
            director= row["director"],
            release_year= row["release_year"],
            rating= row["rating"]
        )
        movies.append(movie)
    return movies

def get_specific_movie(movie_id: int):
    rows = read_query("SELECT id, title, director, release_year, rating FROM movies WHERE id = ?", (movie_id, ))
    
    if not rows:
        return None
    row = rows[0]
    return MovieResponse(
        id = row["id"],
        title= row["title"],
        director= row["director"],
        release_year= row["release_year"],
        rating= row["rating"]
    )
    
def update_movie(movie_id: int, movie_data: MovieUpdate):
    current_movie = get_specific_movie(movie_id)
    if not current_movie:
        return None
    
    title = movie_data.title if movie_data.title is not None else current_movie.title
    director = movie_data.director if movie_data.director is not None else current_movie.director
    release_year = movie_data.release_year if movie_data.release_year is not None else current_movie.release_year
    
    update_query("UPDATE movies SET title = ?, director = ?, release_year = ? WHERE id = ?", (title, director, release_year, movie_id, ))
    return get_specific_movie(movie_id)

def delete_movie(movie_id: int):
    rows = read_query("SELECT id FROM movies WHERE id = ?", (movie_id, ))
    if not rows:
        return False
    update_query("DELETE FROM movies WHERE id = ?", (movie_id, ))
    return True

async def renew_movie_rating(movie_id: int, movie_title: str):
    rating = await take_movie_rating(movie_title)
    if rating is None:
        return
    update_query("UPDATE movies SET rating = ? WHERE id = ?",(rating, movie_id))
    