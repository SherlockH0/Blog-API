# Blog API

## Installation

Dependencies:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python ^3.12](https://www.python.org/)
- [Poetry](https://python-poetry.org/)

### Development

Create local settings file:

```bash
mkdir -p local
cp blogapi/project/settings/templates/settings.dev.py ./local/settings.dev.py
cp blogapi/project/settings/templates/settings.unittest.py ./local/settings.unittest.py
```

Start PostgreSQL with docker:

```bash
make docker-dependencies-only
```

Install the project using poetry, and create superuser:

```bash
make install
make superuser
```

Run local server:

```bash
make runserver
```

To make migrations after changes in the models, run:

```bash
make migrations
```

To migrate, run:

```bash
make migrate
```
