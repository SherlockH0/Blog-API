## --------------------------------------------------------------
## This Makefile contains shortcuts for installing, launching and 
## testing this projects.
##
## All commands, except for docker-dependencies-only, require 
## poetry (See README.md for more details)
## --------------------------------------------------------------

.PHONY: help
help: ## Show this help.
	@cat $(MAKEFILE_LIST) | grep -E '^##*' | cut -c 4-
	@echo ""
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: docker-dependencies-only
docker-dependencies-only: ## Run PostgreSQL and Redis.
	docker-compose -f docker-compose.dev.yml up --force-recreate

.PHONY: install 
install: ## Install the project using poetry.
	poetry install

.PHONY: migrate
migrate: ## Run django's manage.py migrate.
	poetry run python -m blogapi.manage migrate

.PHONY: migrations 
migrations: ## Run django's manage.py makemigrations.
	poetry run python -m blogapi.manage makemigrations
	
.PHONY: runserver
runserver: ## Run django's manage.py runserver.
	poetry run python -m blogapi.manage runserver

.PHONY: shell
shell: ## Run django's manage.py shell.
	poetry run python -m blogapi.manage shell

.PHONY: superuser
superuser: ## Run django's manage.py createsuperuser.
	poetry run python -m blogapi.manage createsuperuser

.PHONY: rq
rq: ## Run django-rq default worker
	poetry run python -m blogapi.manage rqworker default

.PHONY: rqscheduler
rqscheduler: ## Run django-rq scheduler
	poetry run python -m blogapi.manage rqscheduler

.PHONY: update ## Install the project and run migrations.
update: install migrate ;

.PHONY: test
test: ## Run tests with pytest.
	poetry run pytest -v -rs --show-capture=all

.PHONY: test-cov
test-cov:## Run tests with pytest and show coverage.
	poetry run pytest -v -rs --cov --show-capture=all

.PHONY: test-cov-html
test-cov-html: ## Run tests with pytest and generate html coverage.
	poetry run pytest -v -rs --cov --cov-report html
