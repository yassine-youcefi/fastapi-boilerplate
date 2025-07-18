# syntax=docker/dockerfile:1.4

FROM python:3.13.5-slim AS base

# Install build tools, uv, and curl
RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && pip install uv

# Create non-root user
RUN useradd -ms /bin/bash fastapi

WORKDIR /code

# Copy only requirements for dependency install
COPY requirements.txt /code/

# Install dependencies with uv
RUN uv pip install -r requirements.txt --system --no-cache-dir

# --- Final stage ---
FROM python:3.13.5-slim AS final

WORKDIR /code

# Copy installed packages and executables from base
COPY --from=base /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=base /usr/local/bin/ /usr/local/bin/

# Ensure celery is installed and entrypoint is present
RUN pip install --no-cache-dir celery[redis]

# Install curl in final image
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy app source
COPY . /code/

# Create non-root user and set permissions
RUN useradd -ms /bin/bash fastapi && chown -R fastapi /code && chmod -R u+w /code
USER fastapi

EXPOSE 8000

# Set ENV at runtime (not build time)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

CMD ["sh", "-c", "if [ \"$ENVIRONMENT\" = \"dev\" ]; then uvicorn app.main:app --reload --host 0.0.0.0 --port 8000; else uvicorn app.main:app --host 0.0.0.0 --port 8000; fi"]





