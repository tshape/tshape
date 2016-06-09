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

does not work


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
