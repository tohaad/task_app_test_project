# Task API test project

### Local Development

#### Prerequisites
- Docker ([Docker installation guide](https://docs.docker.com/install/#supported-platforms))
- Docker Compose ([Docker Compose installation guide](https://docs.docker.com/compose/install/))

#### Configuring the Environment
You can find all environment variables under ```envs/``` directory. This is how it should look like:
```
envs
├── app.env
├── app.example.env
├── db.env
└── db.example.env
```
To create your own, local env files from examples:
##### app
```bash
$ cp envs/app.example.env envs/app.env
```
##### db
```bash
$ cp envs/db.example.env envs/db.env
```

#### Build the Stack
This can take a while, especially the first time you run this particular command on your development system:
```bash
$ docker-compose build
```

#### Run the Stack
This brings up all services together. The first time it is run it might take a while to get started, but subsequent runs will occur quickly

Open a terminal at the project root and run the following for local development:
```bash
$ docker-compose up -d
```
This command starts the containers in the background and leaves them running

In case you want to aggregate the output of each container use following command:
```bash
$ docker-compose up
```

#### Collect staticfiles
To collect staticfiles for Django and related packages:
```bash
$ docker-compose exec app python manage.py collectstatic --noinput
```

#### Migrate database
To create database schema:
```bash
$ docker-compose exec app python manage.py migrate
```

#### At this point app should be accessible
- Admin panel at [localhost:8000/admin/](http://localhost:8000/admin/)
- API docs at [localhost:8000/api/docs/](http://localhost:8000/api/docs/)

#### Create a superuser
To create superuser:
```bash
$ docker-compose exec app python manage.py createsuperuser
```

#### Stop the Stack
To stop, just:
```bash
$ docker-compose stop
```

#### Start the Stack
To start the stack in case containers are existing use this command:
```bash
$ docker-compose start
```

#### Destroy the Stack
To stop containers and remove containers and networks:
```bash
$ docker-compose down
```
To stop containers and remove containers, networks and local images:
```bash
$ docker-compose down --rmi local
```  
To stop containers and remove containers, networks, local images and volumes:
```bash
$ docker-compose down --rmi local -v
```

### Testing and coverage
#### Tests
This project uses [Pytest](https://docs.pytest.org/en/latest/index.html), a framework for easily building simple and scalable tests

To perform testing just run the following command:
```bash
$ docker-compose run --rm app pytest
```
To run `pytest` in verbose mode you can use `-v` option:
```bash
$ docker-compose run --rm app pytest -v
```

#### Coverage
You can run the ```pytest``` with code ```coverage``` by typing in the following command:
```bash
$ docker-compose run --rm app pytest --cov
```
After that you will see coverage report just below tests results

#### Linters
This project uses [Ruff](https://docs.astral.sh/ruff/) - an extremely fast Python linter and code formatter

To run Ruff linter over the project use this command:
```bash
$ docker-compose run --rm app ruff check
```
To format code using Ruff formatter, run:
```bash
$ docker-compose run --rm app ruff format
```
