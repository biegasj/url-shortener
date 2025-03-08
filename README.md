# FastAPI URL Shortener

A web application that shortens URLs, providing redirection, statistics, and deletion capabilities.

---

## Technologies Used

### Core Framework

- **[FastAPI](https://fastapi.tiangolo.com/)**

### Database & ORM

- **[SQLModel](https://sqlmodel.tiangolo.com/):** Combines SQLAlchemy (ORM) and Pydantic (data validation) for Python
  database interactions.

- **[PostgreSQL](https://www.postgresql.org/)**

### Infrastructure

- **[Alembic](https://alembic.sqlalchemy.org/en/latest/):** Database migration tool.

- **[Docker](https://docs.docker.com/)**

### Other Tools

- **[Poetry](https://python-poetry.org/)**

- **[Pydantic](https://docs.pydantic.dev/latest/)**

- **[uvicorn](https://www.uvicorn.org/)**

### Testing

- **[pytest](https://docs.pytest.org/en/stable/)**

---

# Local development

## Installation

1. **Install Poetry:**

Follow the official [Poetry installation guide](https://python-poetry.org/docs/#installation) if you haven't
installed it already.

2. **Clone the repository:**

```bash
git clone <repository_url>
cd <repository_directory>
```

> [!NOTE]
> If you experience issues with imports in your IDE, set the source roots to the backend directory. Instructions
> for [PyCharm](https://www.jetbrains.com/help/pycharm/configuring-project-structure.html).

3. **Install dependencies:**

```bash
poetry install
```

---

## Running tests

Follow the official [Poetry installation guide](https://python-poetry.org/docs/#installation) if you haven't
installed it already.

```bash
cd <repository_directory>
pytest backend
```

---

# How to run

## Running the project

- Copy .env.sample file fom /env into .env files and populate it with custom entries Run the dev instance

`sudo docker compose -f docker-compose-dev.yml up --build`

- Run prod instance

`sudo docker compose -f docker-compose-prod.yml up --build`

---

## Database migrations

### 1. Create new table

If you have created a new table make sure to import it in **backend/alembic/env.py**. This way alembic will
include it in revision, for example:

`from app.shortener.models.short_url import ShortUrl`

### 2. Create migration files

`docker compose -f docker-compose-dev.yml run backend alembic revision --autogenerate -m "revision message"`

For example:

`docker compose -f docker-compose-dev.yml run backend alembic revision --autogenerate -m "Create ShortUrl table"`

### 3. Run migrations

`docker compose -f docker-compose-dev.yml run backend alembic upgrade head`

###   

> [!NOTE]
> To start fresh with migrations and the database, run:
> 
> ```bash
> docker system prune
> ```
> 
> and, to be sure, run:
> 
> ```bash
> docker volume prune
> ```
> 
> Be cautious, as these commands delete images, cache, and other Docker-related resources.