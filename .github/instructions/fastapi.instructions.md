# .github/copilot.yml

version: 1

# 👨‍💻 General Instructions to steer Copilot behavior

global:

# General coding tone & style

  language: python
  style:
    - Follow clean code principles: short functions, descriptive names, minimal side effects
    - Use FastAPI async-first design
    - Always use PEP8 and black formatting
    - Avoid logic in route handlers — use services instead
    - Use type hints everywhere
    - Add docstrings for all functions and classes
  rules:
    - Use APIRouter for each module's routes under /api/v1
    - Always use async SQLAlchemy ORM and sessions
    - Pydantic schemas for all request/response validation
    - Celery tasks must be idempotent and retryable
    - Use `Depends()` for dependency injection
    - Use environment configs from `config/` directory
    - Use `loguru` or `structlog` for logging

# 📦 Folder-specific instructions

paths:

- path: src/**/routes/**
  rules:

  - All routes must be in APIRouter and prefixed with version (e.g. /api/v1)
  - Never include business logic here — delegate to service layer
  - Use response_model and HTTP status codes
- path: src/**/services/**
  rules:

  - Handle database operations and core business logic here
  - Raise domain exceptions from `exceptions/` module
  - Never depend on FastAPI objects here (no Request or Depends)
- path: src/**/schemas/**
  rules:

  - Define Pydantic models for all input/output schemas
  - Use BaseModelConfig to control orm_mode, aliases, and validation behavior
- path: src/**/models/**
  rules:

  - Use SQLAlchemy 2.0 declarative style
  - All models should inherit from Base
  - Annotate columns with `Mapped[]`
- path: src/**/tasks/**
  rules:

  - Use Celery app and task decorators
  - Define retries, acks_late, and error logging
- path: config/**
  rules:

  - Use Pydantic `BaseSettings` pattern
  - Load environment-specific configs via `.env`

# 🔒 Security Practices

security:
  rules:
    - Never hardcode secrets, use environment variables
    - Always sanitize user input via Pydantic
    - Use OAuth2/JWT best practices for authentication
    - Avoid dynamic `eval()` or unsafe expressions

# 🧪 Testing Guidelines

testing:
  rules:
    - Use pytest with httpx.AsyncClient
    - Fixtures for database and auth tokens
    - Use test-specific database config

# 🐳 Docker / Deployment

deployment:
  rules:
    - Use Dockerfile for multi-stage builds
    - Use docker-compose.yaml for local development stack
    - Set uvicorn worker count in `uvicorn_config/`
