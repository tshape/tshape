PYTHON = /usr/local/bin/python
DOCKER = /usr/local/bin/docker

# runs the web and db containers and starts bash
docker-bash:
	docker-compose run web bash

# rebuilds the container images
docker-build:
	docker-compose build

# cleans up old docker containers and images
# run this occasionally to remove garbage
# must copy and paste the commands into terminal
docker-clean:
	docker rmi $(docker images | grep "^<none>" | awk "{print $3}")
	docker rm $(docker ps -a -q) -v

# shortcut for running django management command
docker-cmd: # include cmd=cmd_name
	docker exec -it tshape_web_1 python manage.py $(cmd)

# starts db container only
# docker-db:
	# docker-compose run db

# gets the ip address of the running docker container
docker-ip:
	docker-machine ip

# runs the postgres container and brings up the postgres shell
docker-postgres:
	docker-compose run db psql -h 192.168.99.100 -p 5432 -U postgres postgres

# forces the containers to be re-built and starts them
docker-recreate:
	docker-compose up --force-recreate

# starts the containers and the application
docker-run:
	docker-compose up

# starts web container only
# docker-web:
	# docker-compose run web

# ____________________________________________________________
# Must be in docker bash before running the following commands:

clean:
	rm -rf build
	rm -rf *~*
	find . | grep -E "(__pycache__|\.pyc)" | xargs rm -rf

clean-tox:
	rm -rf .tox

db-flush:
	$(PYTHON) src/manage.py flush

db-migrate: # include app=app_name
	$(PYTHON) src/manage.py makemigrations $(app)
	$(PYTHON) src/manage.py migrate $(app)

db-reset:
	$(PYTHON) src/manage.py reset_db
	$(PYTHON) src/manage.py syncdb

db-seed:
	$(PYTHON) src/manage.py shell < tests/db/seed_db.py

db-shell:
	psql -h 192.168.99.100 -p 5432 -U postgres postgres

env:
	pyvenv env && ln -s env/bin/activate activate

requirements:
	pip install -r requirements.text

run:
	$(PYTHON) src/manage.py runserver 0.0.0.0:8000

ssl:
	$(PYTHON) src/manage.py runsslserver 0.0.0.0:9000

shell:
	$(PYTHON) src/manage.py shell

syncdb:
	$(PYTHON) src/manage.py syncdb --noinput

test:
	docker-compose -f docker-compose.yml -f docker-compose.debug.yml up

update:
	pip install --upgrade -r requirements.text


# docker commands:
# docker machine - docker-machine create -d virtualbox dev;
#                - eval "$(docker-machine env dev)"
#                - docker-machine ip tshape_web
# bind port to local - docker run -p 0.0.0.0:8000:8000 tshape_web
# example run cmds - docker-compose run web django-admin.py startproject app .
#                  - docker exec -it tshape_web python manage.py migrate (must have containers running)
#                  - docker run python manage.py migrate tshape_web (must have containers running)
