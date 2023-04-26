<div align="center">
  <h1>FastAPI Todos✨</h1>
  <p>FastAPI 🚀 • PostgreSQL 🐘 • SQLAlchemy 💠 • FastAPIUsers 👥</p>
</div>

## Introduction

The app provides a fully async backend web server for to-do apps.


## Technologies used

This project combines the following:

- [`FastAPI`](https://fastapi.tiangolo.com/) for the fast speed web-server and data validation at runtime.
- [`PostgreSQL`](https://www.postgresql.org/) as the database management system (DBMS).
- [`SQLAlchemy`](https://www.sqlalchemy.org/) as the object relational mapper (ORM).
- [`FastAPIUsers`](https://fastapi-users.github.io/fastapi-users/) for registration and authentication system.

... and some [more stuff](./requirements.txt).


## Running locally

### Setting up the project

Clone the repository and navigate to its directory:

    git clone https://github.com/eladgunders/todos_back.git
    cd todos_back

Create and activate a virtual environment

    $ python3 -m venv venv
    $ . venv/bin/activate

Install requirements:

    $ pip3 install -r requirements.txt

Create .env file

    $ touch .env

Fill the following content with your configuration and paste it into the file:
```dotenv
DB_CONN_STR=postgresql+asyncpg://<username>:<password>@<hostname>:5432/<db_name>
ORIGINS=http://localhost:3000;http://127.0.0.1:8000
JWT_SECRET_KEY=<your-secret-key>
JWT_LIFETIME_SECONDS=43200
```

> **Warning**
> This project requires a running instance of PostgreSQL to function properly

### Initiating the database tables
    $ python3 src/init_db.py

### Running the dev server
    $ python3 src/main.py

## License

This project is under the MIT license.
