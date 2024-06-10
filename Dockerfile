# The builder image, used to build the virtual environment
FROM python:3.12-slim-bookworm as builder

ENV POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    PYSETUP_PATH=/opt/pysetup \
    VENV_PATH=/opt/pysetup/.venv

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN pip install poetry==${POETRY_VERSION}

WORKDIR $PYSETUP_PATH

# Project dependencies installation -> cached layer
COPY dataentry-app/pyproject.toml dataentry-app/poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=/root/.cache \
    poetry install --without=dev --no-root

# Project installation Himself
# /!\ modules are installed by poetry in editable mode
# /!\ the whole PYSETUP_PATH is copied to 'runtime' (including modules files)
COPY dataentry-app/modules modules
RUN --mount=type=cache,target=/root/.cache \
    poetry install --without=dev

# RUNTIME IMAGE
FROM python:3.12-slim-bookworm as runtime

ENV PYSETUP_PATH=/opt/pysetup
ENV PATH="$PYSETUP_PATH/.venv/bin:$PATH"

COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

WORKDIR /app
COPY dataentry-app/app.py .

# RUN useradd -m app_user
# USER app_user

EXPOSE 8080
CMD ["marimo", "run", "app.py", "--host", "0.0.0.0", "-p", "8080" ]
