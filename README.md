<div align="center">
  <h1>Todos Back ✨</h1>
  <p>FastApi 🚀 • PostgreSQL 🐘 • SQLAlchemy 💠  </p>
</div>

## Introduction

The app provides a backend web server for to-do apps.


## Technologies used

This project combines the following:

- [`FastApi`](https://fastapi.tiangolo.com/) for the fast speed web-server.
- [`PostgreSQL`](https://www.postgresql.org/) as the database management system (DBMS).
- [`SQLAlchemy`](https://www.sqlalchemy.org/) as the object relational mapper (ORM).
- [`Pydantic`](https://docs.pydantic.dev/) for api data validation at runtime and settings management.
- [`Pylint`](https://readthedocs.org/projects/pylint/) for static code analysis.

... and some [more stuff](./requirements.txt).


## Running locally

### Setting up the project

Clone the repository:

    git clone https://github.com/eladgunders/todos_back.git
    cd todos_back

Create and activate a virtual environment

    $ python3 -m venv venv
    $ . venv/bin/activate

Install requirements:

    $ pip3 install -r requirements.txt

Create .env file

    $ touch .env

Fill the following content with your configuration and Paste it into the file:
```dotenv
DB_CONN_STR=postgresql+asyncpg://<username>:<password>@<hostname>:5432/<db_name>
ORIGINS=http://localhost:3000;http://127.0.0.1:8000
JWT_SECRET_KEY=<your-secret-key>
JWT_LIFETIME_SECONDS=43200
```

> **Alert**
> This project requires a running instance of PostgreSQL to function properly

### Initiating the database tables
    $ python3 src/init_db.py

### Running the dev server
    $ python3 src/main.py