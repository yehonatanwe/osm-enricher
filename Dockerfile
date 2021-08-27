FROM python:3.8-slim as base

RUN apt update && apt -y upgrade

RUN pip install --upgrade pip wheel setuptools packaging poetry virtualenv
RUN poetry config virtualenvs.in-project true

RUN mkdir -p /workspace
WORKDIR /workspace
COPY ./osm_enricher /workspace/osm_enricher
COPY ./tests /workspace/tests
COPY ./poetry.lock /workspace/poetry.lock
COPY ./pyproject.toml /workspace/pyproject.toml
COPY ./osm_enricher_client.py /workspace/osm_enricher_client.py

RUN poetry install


FROM python:3.8-slim

RUN apt update && apt -y upgrade

COPY --from=base /workspace /workspace
WORKDIR /workspace
ENV PYTHONPATH=/workspace/:/workspace/.venv/lib/python3.8/site-packages/

ENTRYPOINT ["python", "./osm_enricher/web_app.py"]