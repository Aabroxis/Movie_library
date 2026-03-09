from fastapi import Query, HTTPException, BackgroundTasks, Depends, APIRouter, status
from auth import admin_required, user_required
from data.models import MovieCreate, MovieResponse, MovieUpdate, TokenData
from services import movie_services

movie_router = APIRouter(prefix="/movies", tags=["Movies"])

@movie_router.post("", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(
    data: MovieCreate,
    background_tasks: BackgroundTasks,
    curr_user: TokenData = Depends(admin_required)
):
    movie = movie_services.create_movie(data)
    background_tasks.add_task(movie_services.renew_movie_rating, movie.id, movie.title)
    return movie

@movie_router.get("", response_model= list[MovieResponse])
def get_all_movies(
    name: str | None = Query(None),
    sorted_by_rating: bool = Query(False),
    curr_user: TokenData = Depends(user_required)
):
    return movie_services.get_all_movies(movie_name=name, sorted_by_rating=sorted_by_rating)

@movie_router.get('/{movie_id}', response_model=MovieResponse)
def get_movie(movie_id: int, curr_user: TokenData = Depends(user_required)):
    movie = movie_services.get_specific_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie

@movie_router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    data: MovieUpdate,
    curr_user: TokenData = Depends(admin_required)
):
    movie = movie_services.update_movie(movie_id, data)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie

@movie_router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, curr_user: TokenData = Depends(admin_required)):
    deleted = movie_services.delete_movie(movie_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")