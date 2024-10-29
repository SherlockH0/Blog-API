.PHONY: docker-dependencies-only
docker-dependencies-only:
	docker-compose -f docker-compose.dev.yml up --force-recreate

.PHONY: install 
install:
	poetry install

.PHONY: migrate
migrate: 
	poetry run python -m blogapi.manage migrate

.PHONY: migrations 
migrations: 
	poetry run python -m blogapi.manage makemigrations
	
.PHONY: runserver
runserver:
	poetry run python -m blogapi.manage runserver

.PHONY: superuser
superuser:
	poetry run python -m blogapi.manage createsuperuser

.PHONY: update
update: install migrate ;

.PHONY: test
test: 
	poetry run pytest -v -rs --cov --show-capture=all

.PHONY: test-cov
test-cov-html: 
	poetry run pytest -v -rs --cov --cov-report html
