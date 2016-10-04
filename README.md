# T-Shape

#### Install
```
git clone https://github.com/angieellis/tshape.git
```

#### Start
- Open Kitematic application
- Click on "DOCKER CLI" in lower left corner
- navigate to project root
- `make docker-build`
- `make docker-run` 
- you will probably see errors in the terminal and in Kitematic tshape_db_1 or tshape_web_1 may not be green.
- shut down the server using ctrl C
- `make docker-recreate`
- now lets seed the database. You need to enter the docker bash for this. 
- `make docker-bash`
- you must be in the directory app/src
- `python manage.py db_seed`
- if the seed does not work you can flush the db using `python manage.py flush`


#### Common Docker Commands
*Recreate and start containers:*
```
make docker-recreate
```

*Start containers and run bash:*
```
make docker-bash
```

*Start containers and run postgres shell:*
```
make docker-postgres
```

*Start containers only:*
```
make docker-run
```

*Build containers only:*
```
make docker-build
```

#### Run These Clean-up Commands Often!
*To remove old images:*
```
docker rmi $(docker images | grep "^<none>" | awk "{print $3}")
```

*To remove old containers:*
```
docker rm $(docker ps -a -q) -v
```
