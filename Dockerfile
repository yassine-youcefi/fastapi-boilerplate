# syntax = docker/dockerfile:1.2.1

FROM python:3.13

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV APP_ENV=development

# Set environment variables for Celery
ENV C_FORCE_ROOT="true"

# Add a new user
RUN useradd -ms /bin/bash fastapi

# Set work directory
WORKDIR /code

# Copy requirements file separately to leverage Docker cache
COPY requirements.txt /code/

# Install dependencies (no need for distutils/setuptools for redis[asyncio])
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the source code
COPY . /code/

# Change ownership to the created user
RUN chown -R fastapi /code
# Make sure the user has write access to the /code directory
RUN chmod -R u+w /code
# Switch to the newly created user
USER fastapi

# Expose port
EXPOSE 8000

# Add HEALTHCHECK instruction
# HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl --fail http://localhost:8000/admin/ || exit 1


# Command to run Uvicorn
# For Development (APP_ENV=development):

#     The command will run Uvicorn with the --reload option and use app/config/uvicorn_conf.py for logging configuration.

# For Production (default case):

#     It will run Uvicorn without the --reload option and use app/config/prod_uvicorn_conf.py for production-specific logging configuration.

CMD ["sh", "-c", "if [ \"$APP_ENV\" = \"development\" ]; then \
    uvicorn app.main:app --reload --log-config app/config/uvicorn_conf.py --host $host --port $port; \
    else uvicorn app.main:app --log-config app/config/prod_uvicorn_conf.py --host $host --port $port; fi"]





