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
