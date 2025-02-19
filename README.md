# FastAPI URL Shortener

A URL shortener service built with FastAPI and SQLModel that creates and manages short URLs for redirection, statistics,
and deletion. The application uses PostgreSQL as its database.

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

## Running tests

Follow the official [Poetry installation guide](https://python-poetry.org/docs/#installation) if you haven't
installed it already.

```bash
pytest backend
```

1. **Install Poetry:**

Follow the official [Poetry installation guide](https://python-poetry.org/docs/#installation) if you haven't
installed it already.

2. **Clone the repository:**

```bash
git clone <repository_url>
cd <repository_directory>
```

3. **Install dependencies:**

```bash
poetry install
```

# How to run

## Running the project

- Copy .env.sample file fom /env into .env files and populate it with custom entries Run the dev instance

`sudo docker compose -f docker-compose-dev.yml up --build`

- Run prod instance

`sudo docker compose -f docker-compose-prod.yml up --build`

## Database

### Migrations

- Create migration file

If you have created **new table** make sure to import it in **backend/alembic/env.py**. This way alembic will
include it in revision.

`from app.models.short_url import ShortUrl`

Then, create migration files.

`docker compose -f docker-compose-dev.yml run backend alembic revision --autogenerate -m "revision message"`

For example

`docker compose -f docker-compose-dev.yml run backend alembic revision --autogenerate -m "Create ShortUrl table"`

- Run migrations, it runs automatically before web server starts

`docker compose -f docker-compose-dev.yml run backend alembic upgrade head`

- If you want to start fresh with migrations and database, run

`docker system prune`

and to be sure

`docker volume prune`

**WARNING** it deletes all images, cache and other docker stuff
