<div align="center">
    <h1>🚀</h1>
  <h1>FastAPI Todos</h1>
  <p>FastAPI 🚀 • PostgreSQL 🐘 • SQLAlchemy 💠 • FastAPIUsers 👥</p>
</div>

## Introduction 🧚

The app provides a fully async backend web server for to-do lists apps.


## Technologies Used 📱

This project combines the following:

- [`FastAPI`](https://fastapi.tiangolo.com/) for the fast speed web-server and data validation at runtime.
- [`PostgreSQL`](https://www.postgresql.org/) as the database management system (DBMS).
- [`SQLAlchemy`](https://www.sqlalchemy.org/) as the object relational mapper (ORM).
- [`FastAPIUsers`](https://fastapi-users.github.io/fastapi-users/) for registration and authentication system.
- [`Docker`](https://docs.docker.com) for containerizing the application.
- [`Docker Compose`](https://docs.docker.com/compose/) for running the project locally in a containerized environment.

... and some [more stuff](./requirements.txt).

## Running Locally 🐳
To run the application locally, you will need to have [Docker](https://docs.docker.com/get-docker/)
and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

Once you have Docker and Docker Compose installed, you can use the following command to start the application:

    $ docker compose up

If everything is working correctly, you should see output in your terminal indicating
that the application is running. You can then access the application from http://localhost:8000.
You can also view the Swagger documentation for the API by visiting http://localhost:8000/docs on your web browser.

## License 📜

This project is under the [MIT license](./LICENSE).
