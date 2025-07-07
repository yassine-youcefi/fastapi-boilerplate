# uvicorn_conf.py

import logging

# Logging configuration
log_level = "debug"  # Verbose logging for easier debugging
access_log = True  # Enable access logs for development debugging
error_log = True  # Enable detailed error logs

# Performance settings (Development-specific)
reload = True  # Enable auto-reloading of the server when code changes

# Network settings for development
host = "0.0.0.0"  # Bind to localhost for development
port = 8000  # Default port for development

# Logging formatting (optional but useful for debugging)
# log_config = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "default": {
#             "()": "uvicorn.logging.DefaultFormatter",
#             "format": "%(asctime)s - %(levelname)s - %(message)s",
#         },
#     },
#     "handlers": {
#         "default": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#             "formatter": "default",
#         },
#     },
#     "loggers": {
#         "uvicorn": {"handlers": ["default"], "level": "DEBUG", "propagate": False},
#         "uvicorn.error": {"handlers": ["default"], "level": "DEBUG", "propagate": False},
#         "uvicorn.access": {"handlers": ["default"], "level": "DEBUG", "propagate": False},
#     },
# }
