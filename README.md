# Blog API

This is a simple blog API with AI moderation features, written in python with Django and Django Ninja.

##### Table of Contents

- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Usage](#usage)
  - [Launching the application in testing mode](#launching-the-application-in-testing-mode)
  - [Development](#development-and-running-tests)
- [API Docs](#api-docs)
  - [Authentication](#authentication)

## Demo

[![Watch the video](https://img.youtube.com/vi/MnOoMGSmVR8/maxresdefault.jpg)](https://youtu.be/MnOoMGSmVR8)

## Tech Stack

- [Django](https://www.djangoproject.com/)
- [Django Ninja](https://django-ninja.dev/)
- [Django RQ](https://github.com/rq/django-rq)
- [Google AI](https://pypi.org/project/google-generativeai/)
- [Pytest](https://docs.pytest.org/en/stable/getting-started.html)
- [Docker](https://www.docker.com/)

## Usage

Clone the repo, and `cd` into it:

```bash
git clone https://github.com/SherlockH0/Blog-API.git
cd Blog-API
```

Then, you can either run the application in testing mode using docker compose, or run the application in development mode.

### Launching the application in testing mode

Make sure you have [Docker](https://www.docker.com/) installed on your system.

Create local settings files:

```bash
mkdir -p local
cp blogapi/project/settings/templates/settings.prod.py ./local/settings.prod.py
```

And set a google AI API key in it (you can omit this step, but the AI features won't work):

```diff
# local/settings.prod.py
- GOOGLE_AI_API_KEY = NotImplemented
+ GOOGLE_AI_API_KEY = "djjnJIJIJhkh"
```

Run the application:

```bash
docker compose up
```

Application is now available on <localhost:8000> (for more routes see [API Docs](#api-docs))

### Development and running tests

Make sure you have [Docker](https://www.docker.com/) and [Python ^3.12](https://www.python.org/) installed on your system.
I'm also using [Poetry](https://python-poetry.org/) as a dependency manager, so if you have it installed on your system, it would be a plus.

Create local settings files:

```bash
mkdir -p local
cp blogapi/project/settings/templates/settings.dev.py ./local/settings.dev.py
cp blogapi/project/settings/templates/settings.unittest.py ./local/settings.unittest.py
```

And add set a google AI API key in both of them (`.dev` file is used for development, and `.unittest` is used for running tests) (you can omit this step, but the AI features won't work):

```diff
# /local/settings.dev.py or /local/settings.unittest.py
- GOOGLE_AI_API_KEY = NotImplemented
+ GOOGLE_AI_API_KEY = "djjnJIJIJhkh"
```

Create and activate virtual environment:

```bash
python -m venv venv
# Linux, MacOS, Windows (WSL)
source venv/bin/activate
# Windows
venv\Scripts\activate.bat
```

In a separate terminal window start PostgreSQL and Redis with docker:

```bash
docker-compose -f docker-compose.dev.yml up --force-recreate
```

Then, continue depending on your system:

<details>
<summary>With Makefile and Poetry (Linux, MacOS, Windows (WSL))</summary>

Install the project using poetry, migrate the database, and create superuser (optional):

```bash
make install
make migrate
make superuser
```

Run local server:

```bash
make runserver
```

In a different terminal window, run rq worker and scheduler:

```bash
make rq
make rqscheduler
```

To make migrations after changes in the models, run:

```bash
make migrations
```

To migrate, run:

```bash
make migrate
```

To run tests, run:

```bash
make test
# With coverage
make test-cov
# With html coverage
make test-cov-html
```

</details>
<details>
<summary>With Poetry (All systems with Poetry installed)</summary>

Install the project using poetry, migrate the database, and create superuser (optional):

```bash
poetry install
poetry run python -m blogapi.manage migrate
poetry run python -m blogapi.manage createsuperuser
```

Run local server:

```bash
poetry run python -m blogapi.manage runserver
```

In a different terminal window, run rq worker and scheduler:

```bash
poetry run python -m blogapi.manage rqworker default
poetry run python -m blogapi.manage rqscheduler
```

To make migrations after changes in the models, run:

```bash
poetry run python -m blogapi.manage makemigrations
```

To migrate, run:

```bash
poetry run python -m blogapi.manage migrate
```

To run tests, run:

```bash
poetry run pytest -v -rs
# With coverage
poetry run pytest -v -rs --cov
# With html coverage
poetry run pytest -v -rs --cov --cov-report html
```

</details>
<details>
<summary>With pip (All systems)</summary>

Install the project using pip, migrate the database, and create superuser (optional):

```bash
pip install .
python -m blogapi.manage migrate
python -m blogapi.manage createsuperuser
```

Run local server:

```bash
python -m blogapi.manage runserver
```

In a different terminal window, run rq worker and scheduler:

```bash
python -m blogapi.manage rqworker default
python -m blogapi.manage rqscheduler
```

To run tests, run:

```bash
pytest -v -rs
# With coverage
pytest -v -rs --cov
# With html coverage
pytest -v -rs --cov --cov-report html
```

</details>

## API Docs

Django-Ninja comes with an easy to use interactive API documentation. If you have launched the application, you can check it out on `localhost:8000/api/docs`.

Django also comes with a featureful admin panel which you can use by visiting `localhost:8000/admin` (you have to create superuser to use it)

### Authentication

Blog-API implements a simple JWT authentication.

To create a user, make a `POST` request to the `/api/users` route.

To log user in, obtain access and refresh tokens by making a `POST` request to the `api/token/pair` route.

To access protected routes, add a `Authorization` header into your request:

```
Authorization: Bearer <token>
```
