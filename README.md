# FastAPI Boilerplate

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/your-repo)

A robust, production-ready FastAPI backend template following best practices for structure, configuration, and development workflow.

---

## 📦 Tech Stack
- **FastAPI**
- **SQLAlchemy (Async)**
- **Alembic**
- **PostgreSQL**
- **Docker & Docker Compose**
- **Redis**
- **pgAdmin**
- **Pydantic**
- **Pre-commit hooks**

---

## 🚀 Features
- Modular project structure for scalability and maintainability
- API versioning for smooth upgrades
- Centralized configuration using Pydantic
- Alembic migrations for database schema management
- JWT authentication ready
- Pre-commit hooks for linting and formatting (`black`, `isort`, `flake8`)
- Docker & Docker Compose support for local and production
- Async SQLAlchemy support
- Environment variable management with `.env`
- pgAdmin integration for easy PostgreSQL management
- Consistent error responses with a top-level `errors` array

---

## 🛠️ Requirements
- Python 3.10+
- Docker & Docker Compose (for containerized development)
- PostgreSQL (local or Docker)

---

## 🗂️ Project Structure
```
fastapi-boilerplate/
├── alembic/                # Database migrations
├── app/
│   ├── auth/               # Authentication domain logic
│   │   ├── models/         # Auth models
│   │   ├── routes/         # Auth routes
│   │   ├── schemas/        # Auth schemas
│   │   ├── services/       # Auth services
│   │   ├── tasks/          # Auth background tasks
│   │   └── utils/          # Auth utilities
│   ├── user/               # User domain logic
│   │   ├── models/         # User models
│   │   ├── routes/         # User routes
│   │   ├── schemas/        # User schemas
│   │   ├── services/       # User services
│   │   ├── tasks/          # User background tasks
│   │   └── utils/          # User utilities
│   ├── config/             # Configuration files
│   ├── utils/              # Shared utilities (e.g., redis_cache)
│   ├── main.py             # App entrypoint
│   ├── dependencies.py     # Dependency injection
│   └── pagination.py       # Pagination utilities
├── scripts/                # Utility scripts
├── tests/                  # Test suite
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker build file
├── docker-compose.yml      # Docker orchestration
├── env.example             # Example environment variables
├── .env                    # Actual environment variables (not committed)
├── .env.pgadmin            # pgAdmin environment variables
├── alembic.ini             # Alembic config
└── README.md
```

---

## ⚡ Quickstart

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

### 4. Run the App (Dev)
```sh
uvicorn app.main:app --reload
```

### 5. Run with Docker Compose
```sh
docker-compose up --build
```

### 6. Enable Pre-commit Hooks
```sh
pre-commit install
```

### 7. Access pgAdmin (optional)
- Visit [http://localhost:5050](http://localhost:5050)
- Login with credentials from `.env.pgadmin`
- Add a new server:
  - **Host:** `db`
  - **Port:** `5432`
  - **Username:** from `.env`
  - **Password:** from `.env`

---

## 🧩 Alembic Migrations
- All SQLAlchemy models in `app/user/models/`, `app/auth/models/`, and other modules are auto-detected by Alembic.
- To create a new migration after changing models:
  ```sh
  alembic revision --autogenerate -m "Describe your change"
  alembic upgrade head
  ```

---

## 🛡️ Error Handling
- All API errors are returned as a top-level `errors` array:
  ```json
  {
    "errors": [
      {
        "error_code": "DUPLICATE_USER_EMAIL",
        "message": "User with email example@domain.com already exists"
      }
    ]
  }
  ```
- Validation errors and custom exceptions follow this format for consistency and easy frontend integration.

---

## 🔑 Example: Authentication API Usage

### Register
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

---

## 🤝 Contributing
- Follow the code style enforced by pre-commit hooks.
- Write tests for new features in the `tests/` directory.
- Use descriptive commit messages.
- Open issues or pull requests for improvements.

---

## 📚 References
- Inspired by [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Happy coding!**

---

## 🚦 CI/CD & Test Coverage

- **Automated CI:** Every push and pull request triggers a GitHub Actions workflow that:
  - Installs dependencies
  - Runs pre-commit hooks (`black`, `isort`, `flake8`)
  - Runs all tests with coverage reporting (`pytest --cov=app tests/`)
  - Uploads a coverage report as an artifact

- **Pre-commit Hooks:** Code style and linting are enforced automatically on every commit and in CI. To enable locally:
  ```sh
  pre-commit install
  ```

- **Test Coverage:**
  - To run tests with coverage locally:
    ```sh
    pytest --cov=app tests/
    ```
  - The CI workflow will fail if tests or code style checks do not pass.

---