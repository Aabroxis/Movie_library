# Movie Library API

Secure FastAPI application for managing a movie catalog with background rating enrichment from OMDb.

## Tech Stack

- **FastAPI** — web framework
- **MariaDB** — database (raw SQL, no ORM)
- **JWT** — authentication (python-jose)
- **bcrypt** — password hashing (passlib)
- **OMDb API** — external movie rating enrichment
- **BackgroundTasks** — async enrichment after response

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create the database in MariaDB:
```sql
CREATE DATABASE movie_library;
USE movie_library;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role ENUM('ADMIN', 'USER') NOT NULL DEFAULT 'USER'
);

CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    director VARCHAR(255),
    release_year SMALLINT,
    rating DECIMAL(3,1)
);
```

3. Configure environment:
```bash
cp .env.example .env
# Fill in your MariaDB credentials and OMDb API key
```

4. Run the server:
```bash
uvicorn main:app --reload
```

## Project Structure
```
Movie_library/
├── data/
│   ├── database.py       # MariaDB connection
│   └── models.py         # Pydantic schemas
├── routers/
│   ├── auth_router.py    # Auth endpoints
│   └── movie_router.py   # Movie endpoints
├── services/
│   ├── auth_services.py  # Auth business logic
│   ├── movie_services.py # Movie business logic
│   └── omdb_services.py  # OMDb API client
├── auth.py               # JWT + role dependencies
├── config.py             # Settings
├── main.py               # App entry point
├── .env                  # Environment variables
└── tests/
    └── test_movie_services.py
```