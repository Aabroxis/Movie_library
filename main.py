from fastapi import FastAPI
from routers.auth_router import auth_router
from routers.movie_router import movie_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(movie_router)