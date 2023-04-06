FROM node:slim as frontend
ENV NODE_OPTIONS=--openssl-legacy-provider
WORKDIR /frontend
COPY frontend .
RUN npm ci
RUN npm run build

FROM python:3.11-slim
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PATH="/opt/venv/bin:$PATH"
WORKDIR /app
RUN python3 -m venv /opt/venv
RUN pip install poetry gunicorn
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt | pip install -r /dev/stdin

COPY src README.md .env gunicorn.conf.py .
COPY --from=frontend /frontend/dist/ ./src/tuinbouwer_server_api/frontend

RUN poetry config virtualenvs.create false \
    && poetry build \
    && pip install dist/*.whl

EXPOSE 8000
CMD [ "gunicorn", "-b", "0.0.0.0", "tuinbouwer_server_api:create_app()" ]
