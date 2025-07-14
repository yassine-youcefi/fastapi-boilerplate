#!/usr/bin/env python
import code
import sys

try:
    from IPython import start_ipython

    ipython_available = True
except ImportError:
    ipython_available = False


def shell():
    # Import commonly used objects
    from app.auth.models import token_models
    from app.integrations.database import SessionLocal
    from app.main import app
    from app.user.models import user_models

    session = SessionLocal()
    banner = (
        "\nFastAPI Interactive Shell\n\n"
        "Available objects:\n"
        "  app       - FastAPI app instance\n"
        "  session   - SQLAlchemy session\n"
        "  user_models, token_models - ORM models\n"
    )
    local_vars = {
        "app": app,
        "session": session,
        "user_models": user_models,
        "token_models": token_models,
    }
    if ipython_available:
        start_ipython(argv=[], user_ns=local_vars)
    else:
        code.interact(banner=banner, local=local_vars)


def main():
    if len(sys.argv) < 2:
        print("Usage: python manage.py <command>")
        sys.exit(1)
    command = sys.argv[1]
    if command == "shell":
        shell()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
