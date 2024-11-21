FROM python:3.11.6-slim AS python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app

# Install poetry and dependencies
FROM python AS poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY pyproject.toml poetry.lock alembic.ini ./
COPY migrations/ ./migrations
RUN poetry install --with populator --no-interaction --no-ansi -vvv

# Final image. Without garbage from poetry
FROM python AS runtime
ENV PATH="/app/.venv/bin:$PATH"
# Copy only what we need from the 'poetry' stage image. Namely, the virtualenv
COPY --from=poetry /app /app
COPY src/ ./src