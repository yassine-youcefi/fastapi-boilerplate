# FastAPI Boilerplate

A robust, production-ready FastAPI backend template following best practices for structure, configuration, and development workflow.

---

## 🚀 Features
- **Modular project structure** for scalability and maintainability
- **API versioning** for smooth upgrades
- **Centralized configuration** using Pydantic
- **Alembic migrations** for database schema management
- **JWT authentication** ready
- **Pre-commit hooks** for linting and formatting (`black`, `isort`, `flake8`)
- **Docker & Docker Compose** support for local and production
- **Async SQLAlchemy** support
- **Environment variable management** with `.env`
- **pgAdmin** integration for easy PostgreSQL management
- **Consistent error responses** with a top-level `errors` array

---

## 🗂️ Project Structure
```
fastapi-boilerplate/
├── alembic/                # Database migrations
├── app/
│   ├── api/                # API routers (versioned)
│   ├── config/             # Configuration files
│   │   └── config.py       # Main app settings
│   ├── database.py         # Database connection setup
│   ├── main.py             # App entrypoint
│   ├── pagination.py       # Pagination utilities
│   ├── shop/               # Shop domain logic
│   └── user/               # User domain logic
│       ├── exceptions.py   # User-specific exception handling
│       ├── dependencies.py # User dependencies
│       └── ...             # Models, routes, schemas, services, utils
├── scripts/                # Utility scripts
├── tests/                  # Test suite
├── requirements.txt        # Python dependencies
├── .pre-commit-config.yaml # Pre-commit hooks config
├── Dockerfile              # Docker build file
├── docker-compose.yml      # Docker orchestration
├── env.example             # Example environment variables
├── .env                    # Actual environment variables (not committed)
├── .env.pgadmin            # pgAdmin environment variables
└── README.md
```

---

## 📝 Guidelines
- Use the app factory pattern (`main.py`) for flexibility.
- Keep business logic modular (e.g., `user/`, `shop/`).
- Store all configuration in `app/config/config.py` and use environment variables for secrets.
- Use Alembic for all database migrations.
- Enforce code quality with pre-commit hooks.
- Use API versioning for all endpoints.
- Use Docker Compose for local development and production parity.
- All API errors are returned as a top-level `errors` array for consistency.

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
- All SQLAlchemy models in `app/user/models/` and other modules are auto-detected by Alembic.
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
        "message": "User with email yani2@skyloov.com already exists"
      }
    ]
  }
  ```
- Validation errors and custom exceptions follow this format for consistency and easy frontend integration.

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

**Happy coding!**