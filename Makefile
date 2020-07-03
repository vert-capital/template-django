SHELL:=/bin/bash
ARGS = $(filter-out $@,$(MAKECMDGOALS))
MAKEFLAGS += --silent
BASE_PATH=${PWD}
PYTHON_EXEC=python
DOCKER_COMPOSE_FILE=$(shell echo -f docker-compose.yml)

up:
	docker-compose ${DOCKER_COMPOSE_FILE} up -d

flake8:
	echo "verify pep8 ..."
	docker-compose ${DOCKER_COMPOSE_FILE} exec app flake8 . && isort . -rc

log:
	docker-compose ${DOCKER_COMPOSE_FILE} logs -f app

stop:
	docker-compose ${DOCKER_COMPOSE_FILE} stop

status:
	docker-compose ${DOCKER_COMPOSE_FILE} ps

restart:
	docker-compose ${DOCKER_COMPOSE_FILE} restart

sh:
	docker-compose ${DOCKER_COMPOSE_FILE} exec ${ARGS} bash

test:
	docker-compose ${DOCKER_COMPOSE_FILE} exec app pytest

psql:
	docker-compose ${DOCKER_COMPOSE_FILE} exec db psql -d database

pgcli:
	docker-compose ${DOCKER_COMPOSE_FILE} exec app pgcli postgres://root:root@db:5432/database

_drop_db:
	docker-compose ${DOCKER_COMPOSE_FILE} stop db
	docker-compose ${DOCKER_COMPOSE_FILE} rm db

_create_db:
	docker-compose ${DOCKER_COMPOSE_FILE} up -d db

recreate_db: _drop_db _create_db

createsuperuser:
	docker-compose ${DOCKER_COMPOSE_FILE} exec app ${PYTHON_EXEC} ./manage.py shell -c "from apps.accounts.models import User; User.objects.create_superuser('root@root.com.br', 'root', first_name='Admin', last_name='Root'); print('Superuser created: root@root.com.br:root')"


migrate:
	docker-compose ${DOCKER_COMPOSE_FILE} exec app ${PYTHON_EXEC} manage.py migrate ${ARGS}

makemigrations:
	docker-compose ${DOCKER_COMPOSE_FILE} exec app ${PYTHON_EXEC} manage.py makemigrations ${ARGS}
	docker-compose ${DOCKER_COMPOSE_FILE} exec app ${PYTHON_EXEC} manage.py migrate

busca_rastreio:
	docker-compose ${DOCKER_COMPOSE_FILE} exec app ${PYTHON_EXEC} manage.py busca_rastreio