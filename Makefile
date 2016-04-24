PYTHON = /usr/local/bin/python
DOCKER = /usr/local/bin/docker

docker-bash:
	docker-compose run web bash

docker-build:
	docker-compose build

docker-clean:
	docker rmi $(docker images | grep "^<none>" | awk "{print $3}")
	docker rm $(docker ps -a -q) -v

docker-pg:
	docker-compose run db bash

docker-run:
	docker-compose up

# ____________________________________________________________
# Must be in docker bash before running the following commands:

clean:
	rm -rf build
	rm -rf *~*
	find . -name '*.pyc|__pycache__|\.cache' -exec rm {} \;

clean-tox:
	rm -rf .tox

db-flush:
	$(PYTHON) manage.py flush

db-seed:
	$(PYTHON) manage.py shell < tests/db/seed_db.py

db-shell:
	psql -h 192.168.99.100 -p 5432 -U postgres postgres

db-migrate: # include app=app_name
	$(PYTHON) manage.py makemigrations $(app)
	$(PYTHON) manage.py migrate $(app)

env:
	pyvenv env && ln -s env/bin/activate activate

requirements:
	pip install -r requirements.text

run:
	$(PYTHON) manage.py runserver 0.0.0.0:8000

ssl:
	$(PYTHON) manage.py runsslserver 0.0.0.0:9000

shell:
	$(PYTHON) manage.py shell

syncdb:
	$(PYTHON) manage.py syncdb --noinput

update:
	pip install --upgrade -r requirements.text


# docker commands:
# bind port to local - docker run -p 0.0.0.0:8000:8000 tshape_web
# example run cmds - docker exec -it tshape_web python manage.py migrate
#                  -  docker-compose run web django-admin.py startproject app .
#                  - docker run python manage.py migrate tshape_web
# docker machine - docker-machine create -d virtualbox dev;
#                - eval "$(docker-machine env dev)"
#                - docker-machine ip tshape_web
