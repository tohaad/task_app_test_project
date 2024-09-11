# Task API test project

### Local Development

#### Prerequisites
- Docker ([Docker installation guide](https://docs.docker.com/install/#supported-platforms))
- Docker Compose ([Docker Compose installation guide](https://docs.docker.com/compose/install/))

#### Configuring the Environment
You can find all environment variables under ```docker/``` directory. This is how it looks like:
```
docker
├── app
│   ...
│   └── .env
└── db
    ...
    └── .env
```
If there are no environment files you can copy it manually from ```env.examples``` directory:
##### app
```bash
$ cp envs.example/app.env docker/app/.env
```
##### db
```bash
$ mkdir docker/db/
```
```bash
$ cp envs.example/db.env docker/db/.env
```

#### Build the Stack
This can take a while, especially the first time you run this particular command on your development system
```bash
$ docker-compose build
```

#### Run the Stack
This brings up all services together. The first time it is run it might take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development
```bash
$ docker-compose up -d
```
This command starts the containers in the background and leaves them running.

In case you want to aggregate the output of each container use following command
```bash
$ docker-compose up
```

#### Collect staticfiles
```bash
$ docker-compose exec app python manage.py collectstatic --noinput
```

#### Migrate database
```bash
$ docker-compose exec app python manage.py migrate
```

#### At this point app should be accessible
- Admin panel at [localhost:8000/admin/](http://localhost:8000/admin/)
- API docs at [localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- API at [localhost:8000/api/](http://localhost:8000/api/)

#### Create a superuser
```bash
$ docker-compose exec app python manage.py createsuperuser
```

#### Stop the Stack
To stop, just
```bash
$ docker-compose stop
```

#### Start the Stack
To start the stack in case containers are existing use this command
```bash
$ docker-compose start
```

#### Destroy the Stack
To stop containers and remove containers and networks
```bash
$ docker-compose down
```
To stop containers and remove containers, networks and local images
```bash
$ docker-compose down --rmi local
```  
To stop containers and remove containers, networks, local images and volumes:
```bash
$ docker-compose down --rmi local -v
```

### Testing and coverage
#### Tests
This project uses the [Pytest](https://docs.pytest.org/en/latest/index.html), a framework for easily building simple and scalable tests.

To perform testing just run the following command
```bash
$ docker-compose run --rm app pytest
```
To run `pytest` in verbose mode you can use `-v` option
```bash
$ docker-compose run --rm app pytest -v
```

#### Coverage
You can run the ```pytest``` with code ```coverage``` by typing in the following command:
```bash
$ docker-compose run --rm app pytest --cov
```
After that you will see coverage report just below tests results
