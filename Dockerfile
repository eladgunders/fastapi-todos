FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH $PWD/todos

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt && \
    rm /requirements.txt

COPY ./todos/app /todos/app
COPY ./alembic.ini /alembic.ini
COPY ./todos/migrations /todos/migrations
COPY ./todos/scripts /todos/scripts

RUN chmod +x /todos/scripts/docker-entrypoint.sh

ENTRYPOINT ["/bin/sh", "/todos/scripts/docker-entrypoint.sh"]