FROM python:3.10

WORKDIR /
RUN pip install --no-cache-dir poetry==1.5.1
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-cache --extras worker

RUN pip install --no-cache-dir git+https://github.com/ciemss/pyciemss.git
COPY workers workers
COPY README.md README.md

ENV REDIS_HOST redis
ENV REDIS_PORT 6379

WORKDIR /workers
CMD rq worker --url redis://$REDIS_HOST:$REDIS_PORT high default low
