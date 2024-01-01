## Introduction
This code has been generated from
[these](https://github.com/idoven/backend-challenge/tree/main) requirements
as part of the technical interview for the startup Idoven.

![screenshot_2023-12-21_18-44-05_296796801](https://github.com/Zeioth/idoven-technical-challenge/assets/3357792/ca0ca91d-f3f3-4163-883d-ae9bf441070c)

## How to use
Install the pre-requirements

```
sudo apt install docker virtualenv
```

Create and enable a virtualenv and install the dependencies with

```sh
cd ~/
python -m venv venv
source ~/venv/bin/activate
pip install -r requirements.txt
```

Start the database

```sh
docker run -e POSTGRES_DB=idovendb -e POSTGRES_USER=apiuser -e POSTGRES_PASSWORD=apipassword -p 5432:5432 -d postgres
```

Start the FastAPI server
```
cd ./app
uvicorn main:app --reload
```

Once the FastAPI server is running you can run the tests

```
cd ./tests
ptw
```
Once you end developing you can stop the virtualenv with
```sh
deactivate
```

### Extra commands
Optionally you can run the project in production mode with

```
APP_ENV=production uvicorn main:app
```

Optionally you can connect to the database in interactive mode with
```
docker ps
docker exec -it <instance-id> psql -U apiuser -d idovendb
```

## Directory structure

```
* app
  * model
    - /schemas.py
    - /models.py
  * view
    - /ecgs.py
    - /users.py
  * controller
    - /db.py
    - /users.py
    - /ecgs.py
* tests
  - /test_ecgs_endpoints.py
  - /test_users_endpoints.py
```

## Capture of requirements
[See here](https://github.com/Zeioth/idoven-technical-challenge/blob/main/requirements.md)

## Development roadmap

* **Friday**: Capture of requirements
* **Monday**: MVP
* **Tuesday**: Missing features
* **Wednesday**: Tests
* **Thursday**: Bug fixes


## Architectural decisions

* This project uses the code conventions [PEP8](https://peps.python.org/pep-0008/).
* This project uses the docstring conventions [Google's python style guide](https://google.github.io/styleguide/pyguide.html).
* The database we use is PostgreSQL.
* The ORM we use is alchemysql.
* The migration tool we use is alembic.
* The database is normalized to Boyce Codd's 3º normal form.
* The database implements foreign key constraints to ensure data integrity.
* Aditional endpoint 'delete-user' to be used by users with the 'admin' role.

## Out of scope

* Database backups.
* Logging system.
* Alert system like prometheus.
* Persistent tokens. In case we plan using a load balancer for the users
microservice in the future, this would be a good idea.
* A logout endoint.
* Using email or telephone as primary key for users would be desireable.
* Before leaving staging, we must modify the tests to self-clean data.
* According to the requirements, admins can create users.
  But the requirements do not specify the fact a admin shouldn't
  probably be able to create users with the role 'admin'.
