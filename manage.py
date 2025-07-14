#!/usr/bin/env python
import code
import sys


def shell():
    # Import commonly used objects
    import asyncio

    from app.auth.models import token_models
    from app.integrations.database import AsyncSessionLocal
    from app.main import app
    from app.user.models import user_models

    async def get_async_session():
        async with AsyncSessionLocal() as session:
            return session

    # Create the session variable by default (for bpython/IPython with top-level await)
    session = None
    try:
        loop = asyncio.get_event_loop()
        session = loop.run_until_complete(get_async_session())
    except Exception:
        pass  # If event loop is already running (e.g., in IPython), session will remain None

    banner = (
        "\nFastAPI Async Interactive Shell (bpython recommended)\n\n"
        "Available objects:\n"
        "  app       - FastAPI app instance\n"
        "  session   - AsyncSession (already created, or use 'await get_async_session()')\n"
        "  get_async_session() - async function to get an AsyncSession\n"
        "  user_models, token_models - ORM models\n\n"
        "In bpython, you can use 'await get_async_session()' to get a session if 'session' is None.\n"
    )
    local_vars = {
        "app": app,
        "get_async_session": get_async_session,
        "session": session,
        "user_models": user_models,
        "token_models": token_models,
        "asyncio": asyncio,
    }
    try:
        import bpython

        bpython.embed(locals_=local_vars, banner=banner)
    except ImportError:
        code.interact(banner=banner, local=local_vars)


def main():
    if len(sys.argv) < 2:
        print("Usage: python manage.py <command>")
        sys.exit(1)
    command = sys.argv[1]
    if command == "shell":
        shell()
    elif command == "makemigrations":
        import subprocess

        msg = sys.argv[2] if len(sys.argv) > 2 else "auto"
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", msg], check=True)
    elif command == "migrate":
        import subprocess

        subprocess.run(["alembic", "upgrade", "head"], check=True)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
