SHELL:=/bin/bash
ARGS = $(filter-out $@,$(MAKECMDGOALS))
MAKEFLAGS += --silent
BASE_PATH=${PWD}
PYTHON_EXEC=python
DOCKER_COMPOSE_FILE=$(shell echo -f docker-compose.yml)

include .env
export $(shell sed 's/=.*//' .env)

show_env:
	# Show wich DOCKER_COMPOSE_FILE and ENV the recipes will user
	# It should be referenced by all other recipes you want it to show.
	# It's only printed once even when more than a recipe executed uses it
	sh -c "if [ \"${ENV_PRINTED:-0}\" != \"1\" ]; \
	then \
		echo DOCKER_COMPOSE_FILE = \"${DOCKER_COMPOSE_FILE}\"; \
		echo OSFLAG = \"${OSFLAG}\"; \
	fi; \
	ENV_PRINTED=1;"

_cp_env_file:
	cp -f .env.sample .env

init: show_env _cp_env_file

_rebuild: show_env
	docker-compose -f ${DOCKER_COMPOSE_FILE} down
	docker-compose -f ${DOCKER_COMPOSE_FILE} build --no-cache --force-rm

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
	docker-compose ${DOCKER_COMPOSE_FILE} exec app pgcli postgres://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}

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