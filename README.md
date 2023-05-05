<div align="center">
  <h1>FastAPI Todos✨</h1>
  <p>FastAPI 🚀 • PostgreSQL 🐘 • SQLAlchemy 💠 • FastAPIUsers 👥</p>
</div>

> **Note**
> 
> This project is currently under development

## Introduction

The app provides a fully async backend web server for to-do apps.


## Technologies Used

This project combines the following:

- [`FastAPI`](https://fastapi.tiangolo.com/) for the fast speed web-server and data validation at runtime.
- [`PostgreSQL`](https://www.postgresql.org/) as the database management system (DBMS).
- [`SQLAlchemy`](https://www.sqlalchemy.org/) as the object relational mapper (ORM).
- [`FastAPIUsers`](https://fastapi-users.github.io/fastapi-users/) for registration and authentication system.

... and some [more stuff](./requirements.txt).


## Running Locally

### Setting up the project

Clone the repository and navigate to its directory:

    git clone https://github.com/eladgunders/fastapi-todos.git
    cd fastapi-todos

Create and activate a virtual environment

    $ python3 -m venv venv
    $ . venv/bin/activate

Install requirements:

    $ pip install -r requirements.txt

Create .env file

    $ touch .env

Fill the following content with your configuration and paste it into the file:
```dotenv
JWT_SECRET_KEY=SECRET
CORS_ORIGINS=http://127.0.0.1:3000;http://127.0.0.1:8000
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin
POSTGRES_HOST=localhost:5432
POSTGRES_DB=app
```

Set up the Python environment

    $ export PYTHONPATH=./todos

### Initiating the database

> **Note**
> 
> This project is currently requires a running instance of PostgreSQL to function properly

Migrate the database

    $ alembic upgrade head
    
Initiate base data

    $ python todos/scripts/initial_data.py

### Running the dev server
    $ python todos/app/main.py

## License

This project is under the MIT license.
