FROM python:3.11.8-slim-bullseye as python

ARG SRC=/src

WORKDIR ${SRC}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ${SRC}/pyproject.toml
COPY ./poetry.lock ${SRC}/poetry.lock

RUN poetry install --no-dev

COPY ./manage.py ${SRC}/manage.py
COPY ./recommendation ${SRC}/recommendation
COPY ./envs ${SRC}/envs


COPY ./docker/api/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/api/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

ENTRYPOINT ["/entrypoint"]
