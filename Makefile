PYTHON = /usr/local/bin/python

docker-bash:
	docker-compose run web bash

docker-clean:
	docker rm -v $(docker ps -a -q)
	docker rmi $(docker images | grep "^<none>" | awk "{print $3}")

docker-run:
	docker-compose up


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
	$(PYTHON) manage.py shell < seed_db.py

db-migrate:
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

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
