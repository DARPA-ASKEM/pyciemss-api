FROM python:3.10

WORKDIR /
RUN pip install --no-cache-dir poetry==1.5.1
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-cache

COPY api api
COPY README.md README.md
WORKDIR /api

EXPOSE 8000
CMD [ "uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]
