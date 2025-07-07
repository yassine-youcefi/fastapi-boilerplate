# FastAPI Boilerplate

A production-ready FastAPI backend template following best practices for structure, configuration, and development workflow.

## Features
- Modular project structure for scalability
- API versioning
- Centralized configuration using Pydantic
- Alembic migrations for database management
- JWT authentication ready
- Pre-commit hooks for linting and formatting (`black`, `isort`, `flake8`)
- Docker-ready
- Async SQLAlchemy support
- Environment variable management with `.env`

## Project Structure
```
fastapi-boilerplate/
├── alembic/                # Database migrations
├── app/
│   ├── api/                # API routers (versioned)
│   ├── config/             # Configuration files
│   │   └── config.py       # Main app settings
│   ├── database.py         # Database connection setup
│   ├── exceptions.py       # Custom exception handlers
│   ├── main.py             # App entrypoint
│   ├── pagination.py       # Pagination utilities
│   ├── shop/               # Shop domain logic
│   └── user/               # User domain logic
├── scripts/                # Utility scripts
├── tests/                  # Test suite
├── requirements.txt        # Python dependencies
├── .pre-commit-config.yaml # Pre-commit hooks config
├── Dockerfile              # Docker build file
├── docker-compose.yml      # Docker orchestration
├── env.example             # Example environment variables
└── README.md
```

## Guidelines
- Use the app factory pattern (`main.py`) for flexibility.
- Keep business logic modular (e.g., `user/`, `shop/`).
- Store all configuration in `app/config/config.py` and use environment variables for secrets.
- Use Alembic for all database migrations.
- Enforce code quality with pre-commit hooks.
- Use API versioning for all endpoints.

## How to Use

### 1. Clone and Install
```sh
git clone <repo-url>
cd fastapi-boilerplate
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Setup
Copy `.env.example` to `.env` and fill in your environment variables:
```sh
cp env.example .env
```

### 3. Database Migrations
```sh
alembic upgrade head
```

### 4. Run the App
```sh
uvicorn app.main:app --reload
```

### 5. Run with Docker
```sh
docker-compose up --build
```

### 6. Enable Pre-commit Hooks
```sh
pre-commit install
```

## Contributing
- Follow the code style enforced by pre-commit hooks.
- Write tests for new features in the `tests/` directory.
- Use descriptive commit messages.

---

This project is inspired by [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices).