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
- **uv** (fast Python dependency manager)

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
- Environment variable management with `.env` (multi-env ready)
- pgAdmin integration for easy PostgreSQL management
- Consistent error responses with a top-level `errors` array
- **Multi-stage Docker build for security and small images**
- **Non-root user in containers**
- **Healthcheck endpoint for Docker and cloud**
- **uv for dependency management**

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
├── Dockerfile              # Docker build file (multi-stage, uv, non-root)
├── docker-compose.yml      # Docker orchestration
├── .dockerignore           # Exclude secrets, tests, build artifacts from image
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
uv pip install -r requirements.txt
```

### 2. Environment Setup (Multi-Env Ready)
Copy `.env.example` to `.env` and fill in your environment variables:
```sh
cp env.example .env
```
- For production, use `.env.production` and inject at runtime (do **not** copy into the image).
- For development, use `.env` or `.env.development`.

### 3. Database Migrations
```sh
alembic upgrade head
```

### 4. Run the App (Dev)
```sh
uvicorn app.main:app --reload
```

### 5. Run with Docker Compose (Recommended)
```sh
docker-compose up --build
```
- The Dockerfile uses a multi-stage build, non-root user, and uv for dependencies.
- The `.dockerignore` ensures secrets, tests, and build artifacts are not copied into the image.
- Environment variables are injected at runtime via Docker Compose.

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

## 🩺 Healthcheck Endpoint
- The app exposes a healthcheck endpoint for Docker and cloud:
  - `GET /health` → `{ "status": "ok" }`
- Used by the Dockerfile's `HEALTHCHECK` instruction.
- You can extend this endpoint for readiness/liveness or DB/Redis checks.

---

## 🧩 Alembic Migrations
- All SQLAlchemy models in `app/user/models/`, `app/auth/models/`, and other modules are auto-detected by Alembic.
- To create a new migration after changing models:
  ```sh
  alembic revision --autogenerate -m "Describe your change"
  alembic upgrade head
  ```

---

## 🐚 Custom Interactive Shell & Management Commands (`manage.py`)

This project includes a custom `manage.py` tool for interactive development and database management, inspired by Django's CLI.

### Interactive Shell
Launch a rich async shell with your FastAPI app context, async DB session, and models pre-imported:

```sh
python manage.py shell
```
- Uses [bpython](https://bpython-interpreter.org/) if installed (recommended), else falls back to the standard shell.
- **Available objects:**
  - `app` — FastAPI app instance
  - `session` — Async SQLAlchemy session (created by default, or use `await get_async_session()`)
  - `get_async_session()` — async function to get a new session
  - `user_models`, `token_models` — ORM models
- **Example usage:**
  ```python
  from app.user.services.user_services import UserService
  user = await UserService(session).get_user_by_id(1)
  print(user)
  ```
- If `session` is `None`, use `await get_async_session()` to create one.

### Database Migration Commands
Run Alembic migrations with familiar commands:

- **Create a new migration (with optional message):**
  ```sh
  python manage.py makemigrations "your message here"
  # or just
  python manage.py makemigrations
  ```
  (If no message is provided, defaults to "auto")

- **Apply all migrations:**
  ```sh
  python manage.py migrate
  ```

---

## 🛡️ Security & Best Practices
- **Never commit real secrets** (`.env` is in `.gitignore`).
- Use strong, random secrets in production (`JWT_SECRET`, `DB_PASSWORD`, etc.).
- Use Docker secrets or environment variables for sensitive data in production.
- The Dockerfile uses a non-root user and multi-stage build for security.
- The `.dockerignore` file prevents secrets, tests, and build artifacts from being copied into the image.
- Do not expose unnecessary ports in production.
- Use resource limits in production deployments.

---

## 🔑 Example: Authentication API Usage

### Register
```http
POST /user/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### Login
```http
POST /user/auth/login
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
- <b style="color:red">Before pushing, you MUST run:</b>
  <pre style="color:red"><code>pre-commit run --all-files
pytest --cov=app tests/
</code></pre>
  <b style="color:red">and ensure all checks pass. This is required for all contributors.</b>

For detailed output and troubleshooting, you can use:
<pre><code>pre-commit run --all-files --verbose --show-diff-on-failure
</code></pre>
This will show exactly what changes each hook would make and help you fix issues before pushing.

---

## 📚 References
- Inspired by [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [uv (Python dependency manager)](https://github.com/astral-sh/uv)

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