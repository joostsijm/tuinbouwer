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

COPY . .

RUN poetry config virtualenvs.create false \
    && poetry build \
    && pip install dist/*.whl

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0" ]
