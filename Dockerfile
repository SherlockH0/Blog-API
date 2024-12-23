FROM python:3.12-bookworm

WORKDIR /opt/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

ENV BLOGAPI_SETTING_DATABASES '{"default":{"HOST":"db"}}'
ENV BLOGAPI_SETTING_LOCAL_SETTINGS_PATH "local/settings.prod.py"
ENV BLOGAPI_SETTING_RQ_QUEUES '{"default": { "HOST": "broker"}}'

RUN set -xe \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install virtualenvwrapper poetry==1.8.3 \ 
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ["poetry.lock", "pyproject.toml", "./"]
RUN poetry install --no-root

COPY ["README.md", "Makefile", "./"]

EXPOSE 8000

COPY scripts scripts
RUN chmod a+x scripts/*

ENTRYPOINT [ "scripts/docker_entrypoint.sh" ]
