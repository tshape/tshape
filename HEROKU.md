# T-Shape 

```
git clone https://github.com/tshape/tshape
```

## Install Python, Django Locally


Install Python 3, Pip & Postgres. You can check your version of Python using `python -V` and `pip -V`


From the project root, the following commands will install the Tshape app locally.

```
virtualenv venv
// or
virtualenv -p python3 venv
```
```
source venv/bin/activate
```
```
pip install requirements.txt
// or
pip install -r requirements.txt
```
```
python src/manage.py collectstatic
```
```
python src/manage.py migrate
```
```
python src/manage.py db_seed
```
```
python src/manage.py runserver 0.0.0.0:8000
```



## Heroku

#### Download & install Heroku CLI 
[Download Heroku CLI Installer] (https://devcenter.heroku.com/articles/heroku-command-line#download-and-install)

```
heroku login
```

#### Create a Heroku remote
[Creating a Heroku remote] (https://devcenter.heroku.com/articles/git#creating-a-heroku-remote)

Instead of using `heroku create` to provision a new app on Heroku, we will be connecting an existing heroku app to our git remote. 

```
heroku git:remote -a tshape
```

You should now see a remote named 'heroku' when you do `git remote -v`

#### Deploying to Heroku

```
git push heroku master
```
This will deploy the local branch 'master' to the Heroku remote.

```
git push heroku localfeaturebranch:master
```
This will deploy any local branch to the Heroku remote.

```
heroku run python src/manage.py migrate
```
```
heroku run python src/manage.py db_seed
```
```
heroku open
```
Will open the live app in the browser

#### Heroku local

Instead of using `runserver 0.0.0.0:8000` to run a local server. You can run `heroku local` which will serve the website locally, using the Gunicorn webserver and Heroku procfile.

#### Heroku Docs
[Getting Started on Heroku with Python] (https://devcenter.heroku.com/articles/getting-started-with-python#introduction)

## Postgres

- [Reinstall Postgres Brew] (https://gist.github.com/mrcasals/2788529)

```
brew install postgres
```
then if you want to automatically run postgresql at login:
```
ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents
```
```
psql
```
```
\l
```

To connect to Postgres locally, you will need to add your local postgres username, database name to the .ENV file in the project root.
